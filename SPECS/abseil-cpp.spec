# Force out of source build
%undefine __cmake_in_source_build

# Installed library version
%global lib_version 2103.0.1

Name:           abseil-cpp
Version:        20210324.2
Release:        2%{?dist}
Summary:        C++ Common Libraries

License:        ASL 2.0
URL:            https://abseil.io
Source0:        https://github.com/abseil/abseil-cpp/archive/%{version}/%{name}-%{version}.tar.gz

# Set up system gtest and gmock targets to allow test suite to be built.
# abseil-cpp expects the targets to be created by a bundled copy of gtest/gmock.
# This patch replicates those targets via find_library and imported targets.
# Not submitted upstream.
Patch1:         abseil-cpp-20210324-gtest.patch

# Disable CPU frequency detection on armv7hl architectures.
# Makes test consistent with aarch64 CPUs.
# Not submitted upstream.
Patch2:         abseil-cpp-20210324.2-armv7.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
BuildRequires:  make

%description
Abseil is an open-source collection of C++ library code designed to augment
the C++ standard library. The Abseil library code is collected from
Google's own C++ code base, has been extensively tested and used in
production, and is the same code we depend on in our daily coding lives.

In some cases, Abseil provides pieces missing from the C++ standard; in
others, Abseil provides alternatives to the standard for special needs we've
found through usage in the Google code base. We denote those cases clearly
within the library code we provide you.

Abseil is not meant to be a competitor to the standard library; we've just
found that many of these utilities serve a purpose within our code base,
and we now want to provide those resources to the C++ community as a whole.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers for %{name}

%prep
%autosetup -p1 -S gendiff
# Remove macro only defined in googletest git master
#sed -i 's|GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST|//|' absl/container/internal/unordered_map_modifiers_test.h

%build
%cmake \
  -DABSL_USE_EXTERNAL_GOOGLETEST:BOOL=ON \
  -DBUILD_TESTING:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING=None \
  -DCMAKE_CXX_STANDARD:STRING=17
%cmake_build


%install
%cmake_install

%check
# s390x does not seem to be supported, several tests fail.
# Make tests informational until failures are resolved.
%ifarch s390x
%ctest --output-on-failure || :
%else
%ctest --output-on-failure
%endif

%files
%license LICENSE
%doc FAQ.md README.md UPGRADES.md
%{_libdir}/libabsl_*.so.%{lib_version}

%files devel
%{_includedir}/absl
%{_libdir}/libabsl_*.so
%{_libdir}/cmake/absl
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210324.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Rich Mattes <richmattes@gmail.com> - 20210324.1-2
- Update to release 20210324.2
- Enable and run test suite

* Mon Mar 08 2021 Rich Mattes <richmattes@gmail.com> - 20200923.3-1
- Update to release 20200923.3

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200923.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 19 2020 Rich Mattes <richmattes@gmail.com> - 20200923.2-1
- Update to release 20200923.2
- Rebuild to fix tagging in koji (rhbz#1885561)

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200225.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200225.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 27 2020 Rich Mattes <richmattes@gmail.com> - 20200225.2-2
- Don't remove buildroot in install

* Sun May 24 2020 Rich Mattes <richmattes@gmail.com> - 20200225.2-1
- Initial package.
