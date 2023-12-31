%ifarch %{power64} s390x
# LuaJIT is not available for POWER and IBM Z
%bcond_with lua_scripting
%else
%bcond_without lua_scripting
%endif

%ifarch x86_64
# VPL/QSV is only available on x86_64
%bcond_without vpl
%else
%bcond_with vpl
%endif

%bcond_without vlc
%bcond_without x264

%global obswebsocket_version 5.3.3
%global origname obs-studio

%if "%{__isa_bits}" == "64"
%global lib64_suffix ()(64bit)
%endif
%global libvlc_soversion 5

Name:           obs-studio-freeworld
Version:        30.0.0
Release:        2%{?dist}
Summary:        Open Broadcaster Software Studio -- Freeworld plugins

# OBS itself is GPL-2.0-or-later, while various plugin dependencies are of various other licenses
# The licenses for those dependencies are captured with the bundled provides statements
License:        GPL-2.0-or-later and MIT and BSD-1-Clause and BSD-2-Clause and BSD-3-Clause and BSL-1.0 and LGPL-2.1-or-later and CC0-1.0 and (CC0-1.0 or OpenSSL or Apache-2.0) and LicenseRef-Fedora-Public-Domain and (BSD-3-Clause or GPL-2.0-only)
URL:            https://obsproject.com/
%if 0%{?snapdate}
Source0:        https://github.com/obsproject/obs-studio/archive/%{commit}/%{origname}-%{commit}.tar.gz
%else
Source0:        https://github.com/obsproject/obs-studio/archive/%{version_no_tilde}/%{origname}-%{version_no_tilde}.tar.gz
%endif
Source1:        https://github.com/obsproject/obs-websocket/archive/%{obswebsocket_version}/obs-websocket-%{obswebsocket_version}.tar.gz

# Backports from upstream

# Proposed upstream
## From: https://github.com/obsproject/obs-studio/pull/8529
Patch0101:      0101-UI-Consistently-reference-the-software-H264-encoder-.patch
Patch0102:      0102-obs-ffmpeg-Add-initial-support-for-the-OpenH264-H.26.patch
Patch0103:      0103-UI-Add-support-for-OpenH264-as-the-worst-case-fallba.patch


# Downstream Fedora patches
## Downgrade to CMake 3.20 for RHEL 9 compatibility
Patch1001:      obs-studio-30-cmake-3.20.patch
## Use fdk-aac by default
Patch1002:      obs-studio-UI-use-fdk-aac-by-default.patch


BuildRequires:  gcc
BuildRequires:  cmake >= 3.20
BuildRequires:  ninja-build
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils

BuildRequires:  alsa-lib-devel
BuildRequires:  asio-devel
BuildRequires:  fdk-aac-free-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  jansson-devel >= 2.5
BuildRequires:  json-devel
BuildRequires:  libcurl-devel
BuildRequires:  libdatachannel-devel
BuildRequires:  libdrm-devel
BuildRequires:  libGL-devel
BuildRequires:  libglvnd-devel
BuildRequires:  librist-devel
BuildRequires:  srt-devel
BuildRequires:  libuuid-devel
BuildRequires:  libv4l-devel
BuildRequires:  libva-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libxkbcommon-devel
%if %{with lua_scripting}
BuildRequires:  luajit-devel
%endif
BuildRequires:  mbedtls-devel
%if %{with vpl}
BuildRequires:  oneVPL-devel
%endif
BuildRequires:  pciutils-devel
BuildRequires:  pipewire-devel
BuildRequires:  pipewire-jack-audio-connection-kit-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  python3-devel
BuildRequires:  libqrcodegencpp-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  speexdsp-devel
BuildRequires:  swig
BuildRequires:  systemd-devel
%if %{with vlc}
BuildRequires:  vlc-devel
%endif
BuildRequires:  wayland-devel
BuildRequires:  websocketpp-devel
%if %{with x264}
BuildRequires:  x264-devel
%endif


# Ensure QtWayland is installed when libwayland-client is installed
Requires:      (qt6-qtwayland%{?_isa} if libwayland-client%{?_isa})
# For icon folder heirarchy
Requires:      hicolor-icon-theme

# These are modified sources that can't be easily unbundled
## License: MIT and CC0-1.0
## Newer version in Fedora with the same licensing
## Request filed upstream for fixing it: https://github.com/simd-everywhere/simde/issues/999
Provides:      bundled(simde) = 0.7.1
## License: BSL-1.0
Provides:      bundled(decklink-sdk)
## License: CC0-1.0 or OpenSSL or Apache-2.0
Provides:      bundled(blake2)
## License: MIT
Provides:      bundled(json11)
## License: MIT
Provides:      bundled(libcaption)
## License: BSD-1-Clause
Provides:      bundled(uthash)
## License: BSD-3-Clause
Provides:      bundled(rnnoise)
## License: LGPL-2.1-or-later and LicenseRef-Fedora-Public-Domain
Provides:      bundled(librtmp)
## License: MIT
Provides:      bundled(libnsgif)
## License: MIT
## Windows only dependency
## Support for Linux will also unbundle it
## Cf. https://github.com/obsproject/obs-studio/pull/8327
Provides:      bundled(intel-mediasdk)

%description
Open Broadcaster Software is free and open source
software for video recording and live streaming.

# --------------------------------------------------------------------------

%package -n obs-studio-plugin-x264
Summary:        Open Broadcaster Software Studio - x264 encoding plugin
License:        GPL-2.0-or-later
BuildRequires:  x264-devel
Requires:       obs-studio%{?_isa} >= %{version}
Supplements:    obs-studio%{?_isa}

%description -n obs-studio-plugin-x264
Open Broadcaster Software is free and open source software
for video recording and live streaming.

This package contains the plugin for using the x264 encoder for
streaming or recording AVC/H.264 video.

%files -n obs-studio-plugin-x264
%license COPYING
%{_libdir}/obs-plugins/obs-x264.so
%{_datadir}/obs/obs-plugins/obs-x264/

# --------------------------------------------------------------------------

%package -n obs-studio-plugin-vlc-video
Summary:        Open Broadcaster Software Studio - VLC-based video plugin
License:        GPL-2.0-or-later
BuildRequires:  vlc-devel
# We dlopen() libvlc
Requires:       libvlc.so.%{libvlc_soversion}%{?lib64_suffix}
Requires:       obs-studio%{?_isa} >= %{version}
Supplements:    obs-studio%{?_isa}


%description -n obs-studio-plugin-vlc-video
Open Broadcaster Software is free and open source software
for video recording and live streaming.

This package contains the plugin for using VLC to embed video
as an overlay in a video stream or recording.

%files -n obs-studio-plugin-vlc-video
%license COPYING
%{_libdir}/obs-plugins/vlc-video.so
%{_datadir}/obs/obs-plugins/vlc-video/

# --------------------------------------------------------------------------


%prep
%setup -q -n %{origname}-%{?snapdate:%{commit}}%{!?snapdate:%{version_no_tilde}}
# Prepare plugins/obs-websocket
tar -xf %{SOURCE1} -C plugins/obs-websocket --strip-components=1
%autopatch -p1

# rpmlint reports E: hardcoded-library-path
# replace OBS_MULTIARCH_SUFFIX by LIB_SUFFIX
sed -e 's|OBS_MULTIARCH_SUFFIX|LIB_SUFFIX|g' -i cmake/Modules/ObsHelpers.cmake

# Kill rpath settings
sed -e '\|set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/${OBS_LIBRARY_DESTINATION}")|d' -i cmake/Modules/ObsHelpers_Linux.cmake

# touch the missing submodules
touch plugins/obs-browser/CMakeLists.txt

%if ! %{with vpl}
# disable unusable qsv plugin
mv plugins/obs-qsv11/CMakeLists.txt plugins/obs-qsv11/CMakeLists.txt.disabled
touch plugins/obs-qsv11/CMakeLists.txt
%endif

# remove -Werror flag to mitigate FTBFS with ffmpeg 5.1
sed -e 's|-Werror-implicit-function-declaration||g' -i cmake/Modules/CompilerConfig.cmake
sed -e '/-Werror/d' -i cmake/Modules/CompilerConfig.cmake

# Removing unused third-party deps
rm -rf deps/w32-pthreads
rm -rf deps/ipc-util
rm -rf deps/jansson

# Remove unneeded EGL/KHR files
rm -rf deps/glad/include/{EGL,KHR}
sed -e 's|include/EGL/eglplatform.h||g' -i deps/glad/CMakeLists.txt

# Collect license files
mkdir -p .fedora-rpm/licenses/deps
mkdir -p .fedora-rpm/licenses/plugins
cp plugins/obs-filters/rnnoise/COPYING .fedora-rpm/licenses/deps/rnnoise-COPYING
cp plugins/obs-websocket/LICENSE .fedora-rpm/licenses/plugins/obs-websocket-LICENSE
cp plugins/obs-outputs/librtmp/COPYING .fedora-rpm/licenses/deps/librtmp-COPYING
cp deps/json11/LICENSE.txt .fedora-rpm/licenses/deps/json11-LICENSE.txt
cp deps/libcaption/LICENSE.txt .fedora-rpm/licenses/deps/libcaption-LICENSE.txt
cp plugins/obs-qsv11/QSV11-License-Clarification-Email.txt .fedora-rpm/licenses/plugins/QSV11-License-Clarification-Email.txt
cp deps/uthash/uthash/LICENSE .fedora-rpm/licenses/deps/uthash-LICENSE
cp deps/blake2/LICENSE.blake2 .fedora-rpm/licenses/deps/
cp deps/media-playback/LICENSE.media-playback .fedora-rpm/licenses/deps/
cp libobs/graphics/libnsgif/LICENSE.libnsgif .fedora-rpm/licenses/deps/
cp libobs/util/simde/LICENSE.simde .fedora-rpm/licenses/deps/
cp plugins/decklink/LICENSE.decklink-sdk .fedora-rpm/licenses/deps
cp plugins/obs-qsv11/obs-qsv11-LICENSE.txt .fedora-rpm/licenses/plugins/


%build
%cmake -DOBS_VERSION_OVERRIDE=%{version_no_tilde} \
       -DUNIX_STRUCTURE=1 -GNinja \
       -DCMAKE_SKIP_RPATH=1 \
       -DBUILD_BROWSER=OFF \
%if ! %{with vlc}
       -DENABLE_VLC=OFF \
%endif
       -DENABLE_JACK=ON \
       -DENABLE_LIBFDK=ON \
       -DENABLE_AJA=OFF \
%if ! %{with lua_scripting}
       -DDISABLE_LUA=ON \
%endif
       -DOpenGL_GL_PREFERENCE=GLVND
%cmake_build


%install
%cmake_install

mkdir -p preserve/%{_libdir}/obs-plugins
mkdir -p preserve/%{_datadir}/obs/obs-plugins

# Preserve plugin files to install
mv %{buildroot}%{_libdir}/obs-plugins/obs-x264.so preserve/%{_libdir}/obs-plugins
mv %{buildroot}%{_datadir}/obs/obs-plugins/obs-x264 preserve/%{_datadir}/obs/obs-plugins
mv %{buildroot}%{_libdir}/obs-plugins/vlc-video.so preserve/%{_libdir}/obs-plugins
mv %{buildroot}%{_datadir}/obs/obs-plugins/vlc-video preserve/%{_datadir}/obs/obs-plugins

# Purge installed buildroot
rm -rf %{buildroot}/*

# Re-install preserved plugins
mv preserve/%{_prefix} %{buildroot}


%changelog
* Thu Nov 16 2023 Dominik Mierzejewski <dominik@greysector.net> - 30.0.0-2
- sync with Fedora

* Wed Nov 15 2023 Nicolas Chauvet <kwizart@gmail.com> - 30.0.0-1
- Update to 30.0.0

* Tue Jul 25 2023 Dominik Mierzejewski <dominik@greysector.net> - 29.1.3-1
- Update to 29.1.3

* Tue Jul 04 2023 Dominik Mierzejewski <dominik@greysector.net> - 29.1.2-1
- Update to 29.1.2

* Thu May 04 2023 Neal Gompa <ngompa@fedoraproject.org> - 29.1.0-1
- Update to 29.1.0 final

* Wed Apr 19 2023 Neal Gompa <ngompa@fedoraproject.org> - 29.1.0~beta4-0.1
- Initial split package from obs-studio
