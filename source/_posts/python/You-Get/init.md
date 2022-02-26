---
title: macOS High Sierra 安装 You-Get 神器
date: 2020-09-10 22:59:25
tags:
  - macOS
  - You-Get
count: 1
os: 1
os_1: High Sierra 10.13.6 (17G65)
browser: 0
browser_0: 85.0.4183.102 Stable
place: 新家
key: 98
---
    Fork you
<!-- more -->
## 0x00.安装
`brew install ffmpeg`

<details><summary>点击此处 ← 查看终端</summary>

``` bash
MacPro:~ yuangezhizao$ brew install ffmpeg
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/aom-1.0.0.high_sierra.
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/dav1d-0.7.0.high_sierr
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libpng-1.6.37.high_sie
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/freetype-2.10.1.high_s
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/fontconfig-2.13.1.high
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/frei0r-1.7.0.high_sier
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/lame-3.100.high_sierra
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/fribidi-1.0.9.high_sie
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/pcre-8.44.high_sierra.
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/gdbm-1.18.1.high_sierr
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/readline-8.0.4.high_si
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/sqlite-3.31.1.high_sie
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/xz-5.2.5.high_sierra.b
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/python%403.8-3.8.2.hig
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/glib-2.64.3.high_sierr
==> Downloading from https://d29vzk4ow07wi7.cloudfront.net/1e5fadb54980899f293ea99796c33f25109c72ad7
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/lzo-2.10.high_sierra.b
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/pixman-0.40.0.high_sie
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/cairo-1.16.0_3.high_si
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/graphite2-1.3.14.high_
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/icu4c-66.1.high_sierra
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/harfbuzz-2.6.6.high_si
==> Downloading from https://d29vzk4ow07wi7.cloudfront.net/9339baeb14615890e90b8c06c081603b9375fa973
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libass-0.14.0_1.high_s
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libbluray-1.2.0.high_s
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libsoxr-0.1.3.high_sie
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libvidstab-1.1.0.high_
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libogg-1.3.4.high_sier
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libvorbis-1.3.6.high_s
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libvpx-1.8.2.high_sier
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/opencore-amr-0.1.5.hig
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/jpeg-9d.high_sierra.bo
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libtiff-4.1.0.high_sie
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/little-cms2-2.9.high_s
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/openjpeg-2.3.1.high_si
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/opus-1.3.1.high_sierra
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/rtmpdump-2.4%2B2015122
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/flac-1.3.3.high_sierra
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libsndfile-1.0.28.high
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libsamplerate-0.1.9_1.
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/rubberband-1.8.2_1.hig
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/sdl2-2.0.12_1.high_sie
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/snappy-1.1.8.high_sier
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/speex-1.2.0.high_sierr
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/srt-1.4.1.high_sierra.
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/giflib-5.2.1.high_sier
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/webp-1.1.0.high_sierra
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/leptonica-1.79.0.high_
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/tesseract-4.1.1.high_s
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/theora-1.1.1.high_sier
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/isl-0.22.1.high_sierra
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/mpfr-4.0.2.high_sierra
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/libmpc-1.1.0.high_sier
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/gcc-9.3.0_1.high_sierr
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/x264-r2999.high_sierra
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/x265-3.3.high_sierra.b
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/xvid-1.3.7.high_sierra
######################################################################## 100.0%
==> Downloading https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/bottles/ffmpeg-4.2.3.high_sier
==> Downloading from https://d29vzk4ow07wi7.cloudfront.net/9d895f4cde8d14d9dc781cf030c07b4263a7d7ce4
######################################################################## 100.0%
==> Installing dependencies for ffmpeg: aom, dav1d, libpng, freetype, fontconfig, frei0r, lame, fribidi, pcre, gdbm, readline, sqlite, xz, python@3.8, glib, lzo, pixman, cairo, graphite2, icu4c, harfbuzz, libass, libbluray, libsoxr, libvidstab, libogg, libvorbis, libvpx, opencore-amr, jpeg, libtiff, little-cms2, openjpeg, opus, rtmpdump, flac, libsndfile, libsamplerate, rubberband, sdl2, snappy, speex, srt, giflib, webp, leptonica, tesseract, theora, isl, mpfr, libmpc, gcc, x264, x265 and xvid
==> Installing ffmpeg dependency: aom
==> Pouring aom-1.0.0.high_sierra.bottle.1.tar.gz
🍺  /usr/local/Cellar/aom/1.0.0: 19 files, 12.6MB
==> Installing ffmpeg dependency: dav1d
==> Pouring dav1d-0.7.0.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/dav1d/0.7.0: 15 files, 1.3MB
==> Installing ffmpeg dependency: libpng
==> Pouring libpng-1.6.37.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libpng/1.6.37: 27 files, 1.2MB
==> Installing ffmpeg dependency: freetype
==> Pouring freetype-2.10.1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/freetype/2.10.1: 61 files, 2.2MB
==> Installing ffmpeg dependency: fontconfig
==> Pouring fontconfig-2.13.1.high_sierra.bottle.tar.gz
==> Regenerating font cache, this may take a while
==> /usr/local/Cellar/fontconfig/2.13.1/bin/fc-cache -frv
🍺  /usr/local/Cellar/fontconfig/2.13.1: 531 files, 3.3MB
==> Installing ffmpeg dependency: frei0r
==> Pouring frei0r-1.7.0.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/frei0r/1.7.0: 128 files, 1.8MB
==> Installing ffmpeg dependency: lame
==> Pouring lame-3.100.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/lame/3.100: 27 files, 2.1MB
==> Installing ffmpeg dependency: fribidi
==> Pouring fribidi-1.0.9.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/fribidi/1.0.9: 67 files, 601KB
==> Installing ffmpeg dependency: pcre
==> Pouring pcre-8.44.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/pcre/8.44: 204 files, 5.5MB
==> Installing ffmpeg dependency: gdbm
==> Pouring gdbm-1.18.1.high_sierra.bottle.1.tar.gz
🍺  /usr/local/Cellar/gdbm/1.18.1: 20 files, 590.8KB
==> Installing ffmpeg dependency: readline
==> Pouring readline-8.0.4.high_sierra.bottle.tar.gz
==> Caveats
readline is keg-only, which means it was not symlinked into /usr/local,
because macOS provides BSD libedit.

For compilers to find readline you may need to set:
  export LDFLAGS="-L/usr/local/opt/readline/lib"
  export CPPFLAGS="-I/usr/local/opt/readline/include"

==> Summary
🍺  /usr/local/Cellar/readline/8.0.4: 48 files, 1.5MB
==> Installing ffmpeg dependency: sqlite
==> Pouring sqlite-3.31.1.high_sierra.bottle.tar.gz
==> Caveats
sqlite is keg-only, which means it was not symlinked into /usr/local,
because macOS already provides this software and installing another version in
parallel can cause all kinds of trouble.

If you need to have sqlite first in your PATH run:
  echo 'export PATH="/usr/local/opt/sqlite/bin:$PATH"' >> /Users/yuangezhizao/.bash_profile

For compilers to find sqlite you may need to set:
  export LDFLAGS="-L/usr/local/opt/sqlite/lib"
  export CPPFLAGS="-I/usr/local/opt/sqlite/include"

==> Summary
🍺  /usr/local/Cellar/sqlite/3.31.1: 11 files, 4MB
==> Installing ffmpeg dependency: xz
==> Pouring xz-5.2.5.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/xz/5.2.5: 92 files, 1.1MB
==> Installing ffmpeg dependency: python@3.8
==> Pouring python@3.8-3.8.2.high_sierra.bottle.tar.gz
==> /usr/local/Cellar/python@3.8/3.8.2/bin/python3 -s setup.py --no-user-cfg install --force --verbo
==> /usr/local/Cellar/python@3.8/3.8.2/bin/python3 -s setup.py --no-user-cfg install --force --verbo
==> /usr/local/Cellar/python@3.8/3.8.2/bin/python3 -s setup.py --no-user-cfg install --force --verbo
==> Caveats
Python has been installed as
  /usr/local/opt/python@3.8/bin/python3

You can install Python packages with
  /usr/local/opt/python@3.8/bin/pip3 install <package>
They will install into the site-package directory
  /usr/local/opt/python@3.8/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages

See: https://docs.brew.sh/Homebrew-and-Python

python@3.8 is keg-only, which means it was not symlinked into /usr/local,
because this is an alternate version of another formula.

If you need to have python@3.8 first in your PATH run:
  echo 'export PATH="/usr/local/opt/python@3.8/bin:$PATH"' >> /Users/yuangezhizao/.bash_profile

For compilers to find python@3.8 you may need to set:
  export LDFLAGS="-L/usr/local/opt/python@3.8/lib"

==> Summary
🍺  /usr/local/Cellar/python@3.8/3.8.2: 4,124 files, 62.8MB
==> Installing ffmpeg dependency: glib
==> Pouring glib-2.64.3.high_sierra.bottle.tar.gz
==> Caveats
Bash completion has been installed to:
  /usr/local/etc/bash_completion.d
==> Summary
🍺  /usr/local/Cellar/glib/2.64.3: 436 files, 15.7MB
==> Installing ffmpeg dependency: lzo
==> Pouring lzo-2.10.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/lzo/2.10: 31 files, 556.5KB
==> Installing ffmpeg dependency: pixman
==> Pouring pixman-0.40.0.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/pixman/0.40.0: 14 files, 1.3MB
==> Installing ffmpeg dependency: cairo
==> Pouring cairo-1.16.0_3.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/cairo/1.16.0_3: 117 files, 5.5MB
==> Installing ffmpeg dependency: graphite2
==> Pouring graphite2-1.3.14.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/graphite2/1.3.14: 18 files, 232.2KB
==> Installing ffmpeg dependency: icu4c
==> Pouring icu4c-66.1.high_sierra.bottle.tar.gz
==> Caveats
icu4c is keg-only, which means it was not symlinked into /usr/local,
because macOS provides libicucore.dylib (but nothing else).

If you need to have icu4c first in your PATH run:
  echo 'export PATH="/usr/local/opt/icu4c/bin:$PATH"' >> /Users/yuangezhizao/.bash_profile
  echo 'export PATH="/usr/local/opt/icu4c/sbin:$PATH"' >> /Users/yuangezhizao/.bash_profile

For compilers to find icu4c you may need to set:
  export LDFLAGS="-L/usr/local/opt/icu4c/lib"
  export CPPFLAGS="-I/usr/local/opt/icu4c/include"

==> Summary
🍺  /usr/local/Cellar/icu4c/66.1: 258 files, 70.6MB
==> Installing ffmpeg dependency: harfbuzz
==> Pouring harfbuzz-2.6.6.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/harfbuzz/2.6.6: 165 files, 11.4MB
==> Installing ffmpeg dependency: libass
==> Pouring libass-0.14.0_1.high_sierra.bottle.1.tar.gz
🍺  /usr/local/Cellar/libass/0.14.0_1: 10 files, 509.4KB
==> Installing ffmpeg dependency: libbluray
==> Pouring libbluray-1.2.0.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libbluray/1.2.0: 21 files, 1.6MB
==> Installing ffmpeg dependency: libsoxr
==> Pouring libsoxr-0.1.3.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libsoxr/0.1.3: 28 files, 242.4KB
==> Installing ffmpeg dependency: libvidstab
==> Pouring libvidstab-1.1.0.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libvidstab/1.1.0: 25 files, 132.0KB
==> Installing ffmpeg dependency: libogg
==> Pouring libogg-1.3.4.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libogg/1.3.4: 97 files, 473.0KB
==> Installing ffmpeg dependency: libvorbis
==> Pouring libvorbis-1.3.6.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libvorbis/1.3.6: 157 files, 2.3MB
==> Installing ffmpeg dependency: libvpx
==> Pouring libvpx-1.8.2.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libvpx/1.8.2: 17 files, 3MB
==> Installing ffmpeg dependency: opencore-amr
==> Pouring opencore-amr-0.1.5.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/opencore-amr/0.1.5: 17 files, 644KB
==> Installing ffmpeg dependency: jpeg
==> Pouring jpeg-9d.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/jpeg/9d: 21 files, 743KB
==> Installing ffmpeg dependency: libtiff
==> Pouring libtiff-4.1.0.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libtiff/4.1.0: 247 files, 3.6MB
==> Installing ffmpeg dependency: little-cms2
==> Pouring little-cms2-2.9.high_sierra.bottle.1.tar.gz
🍺  /usr/local/Cellar/little-cms2/2.9: 18 files, 1MB
==> Installing ffmpeg dependency: openjpeg
==> Pouring openjpeg-2.3.1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/openjpeg/2.3.1: 516 files, 12.8MB
==> Installing ffmpeg dependency: opus
==> Pouring opus-1.3.1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/opus/1.3.1: 17 files, 983.3KB
==> Installing ffmpeg dependency: rtmpdump
==> Pouring rtmpdump-2.4+20151223_1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/rtmpdump/2.4+20151223_1: 20 files, 422.8KB
==> Installing ffmpeg dependency: flac
==> Pouring flac-1.3.3.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/flac/1.3.3: 53 files, 2.4MB
==> Installing ffmpeg dependency: libsndfile
==> Pouring libsndfile-1.0.28.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libsndfile/1.0.28: 48 files, 1.8MB
==> Installing ffmpeg dependency: libsamplerate
==> Pouring libsamplerate-0.1.9_1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libsamplerate/0.1.9_1: 28 files, 3.0MB
==> Installing ffmpeg dependency: rubberband
==> Pouring rubberband-1.8.2_1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/rubberband/1.8.2_1: 12 files, 634.0KB
==> Installing ffmpeg dependency: sdl2
==> Pouring sdl2-2.0.12_1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/sdl2/2.0.12_1: 89 files, 4.7MB
==> Installing ffmpeg dependency: snappy
==> Pouring snappy-1.1.8.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/snappy/1.1.8: 18 files, 119.6KB
==> Installing ffmpeg dependency: speex
==> Pouring speex-1.2.0.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/speex/1.2.0: 21 files, 689KB
==> Installing ffmpeg dependency: srt
==> Pouring srt-1.4.1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/srt/1.4.1: 20 files, 3.6MB
==> Installing ffmpeg dependency: giflib
==> Pouring giflib-5.2.1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/giflib/5.2.1: 19 files, 355.6KB
==> Installing ffmpeg dependency: webp
==> Pouring webp-1.1.0.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/webp/1.1.0: 39 files, 2.1MB
==> Installing ffmpeg dependency: leptonica
==> Pouring leptonica-1.79.0.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/leptonica/1.79.0: 51 files, 5.9MB
==> Installing ffmpeg dependency: tesseract
==> Pouring tesseract-4.1.1.high_sierra.bottle.tar.gz
==> Caveats
This formula contains only the "eng", "osd", and "snum" language data files.
If you need any other supported languages, run `brew install tesseract-lang`.
==> Summary
🍺  /usr/local/Cellar/tesseract/4.1.1: 65 files, 29.9MB
==> Installing ffmpeg dependency: theora
==> Pouring theora-1.1.1.high_sierra.bottle.2.tar.gz
🍺  /usr/local/Cellar/theora/1.1.1: 97 files, 2MB
==> Installing ffmpeg dependency: isl
==> Pouring isl-0.22.1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/isl/0.22.1: 72 files, 4.7MB
==> Installing ffmpeg dependency: mpfr
==> Pouring mpfr-4.0.2.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/mpfr/4.0.2: 28 files, 4.7MB
==> Installing ffmpeg dependency: libmpc
==> Pouring libmpc-1.1.0.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/libmpc/1.1.0: 12 files, 353.8KB
==> Installing ffmpeg dependency: gcc
==> Pouring gcc-9.3.0_1.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/gcc/9.3.0_1: 1,463 files, 289.7MB
==> Installing ffmpeg dependency: x264
==> Pouring x264-r2999.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/x264/r2999: 11 files, 5.6MB
==> Installing ffmpeg dependency: x265
==> Pouring x265-3.3.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/x265/3.3: 11 files, 35.5MB
==> Installing ffmpeg dependency: xvid
==> Pouring xvid-1.3.7.high_sierra.bottle.tar.gz
🍺  /usr/local/Cellar/xvid/1.3.7: 10 files, 1.3MB
==> Installing ffmpeg
==> Pouring ffmpeg-4.2.3.high_sierra.bottle.tar.gz
Warning: ffmpeg dependency gcc was built with a different C++ standard
library (libstdc++ from clang). This may cause problems at runtime.
🍺  /usr/local/Cellar/ffmpeg/4.2.3: 287 files, 57.6MB
==> Caveats
==> readline
readline is keg-only, which means it was not symlinked into /usr/local,
because macOS provides BSD libedit.

For compilers to find readline you may need to set:
  export LDFLAGS="-L/usr/local/opt/readline/lib"
  export CPPFLAGS="-I/usr/local/opt/readline/include"

==> sqlite
sqlite is keg-only, which means it was not symlinked into /usr/local,
because macOS already provides this software and installing another version in
parallel can cause all kinds of trouble.

If you need to have sqlite first in your PATH run:
  echo 'export PATH="/usr/local/opt/sqlite/bin:$PATH"' >> /Users/yuangezhizao/.bash_profile

For compilers to find sqlite you may need to set:
  export LDFLAGS="-L/usr/local/opt/sqlite/lib"
  export CPPFLAGS="-I/usr/local/opt/sqlite/include"

==> python@3.8
Python has been installed as
  /usr/local/opt/python@3.8/bin/python3

You can install Python packages with
  /usr/local/opt/python@3.8/bin/pip3 install <package>
They will install into the site-package directory
  /usr/local/opt/python@3.8/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages

See: https://docs.brew.sh/Homebrew-and-Python

python@3.8 is keg-only, which means it was not symlinked into /usr/local,
because this is an alternate version of another formula.

If you need to have python@3.8 first in your PATH run:
  echo 'export PATH="/usr/local/opt/python@3.8/bin:$PATH"' >> /Users/yuangezhizao/.bash_profile

For compilers to find python@3.8 you may need to set:
  export LDFLAGS="-L/usr/local/opt/python@3.8/lib"

==> glib
Bash completion has been installed to:
  /usr/local/etc/bash_completion.d
==> icu4c
icu4c is keg-only, which means it was not symlinked into /usr/local,
because macOS provides libicucore.dylib (but nothing else).

If you need to have icu4c first in your PATH run:
  echo 'export PATH="/usr/local/opt/icu4c/bin:$PATH"' >> /Users/yuangezhizao/.bash_profile
  echo 'export PATH="/usr/local/opt/icu4c/sbin:$PATH"' >> /Users/yuangezhizao/.bash_profile

For compilers to find icu4c you may need to set:
  export LDFLAGS="-L/usr/local/opt/icu4c/lib"
  export CPPFLAGS="-I/usr/local/opt/icu4c/include"

==> tesseract
This formula contains only the "eng", "osd", and "snum" language data files.
If you need any other supported languages, run `brew install tesseract-lang`.
```

</details>

## 0x01.使用

<details><summary>点击此处 ← 查看终端</summary>

``` bash
MacPro:Downloads yuangezhizao$ you-get https://www.youtube.com/watch?v=2pm28PVSYBc --debug -s 127.0.0.1:1080
[DEBUG] get_content: https://www.youtube.com/get_video_info?video_id=2pm28PVSYBc&eurl=https%3A%2F%2Fy
[DEBUG] STATUS: ok
[DEBUG] get_content: https://www.youtube.com/watch?v=2pm28PVSYBc
[DEBUG] get_content: https://www.youtube.com/s/player/4e193593/player_ias.vflset/en_US/base.js
site:                YouTube
title:               【ラピスリライツ】LiGHTs「私の名は、光。」特別編集版MV（フルサイズver）
stream:
    - itag:          137
      container:     mp4
      quality:       1920x1080 (1080p)
      size:          108.4 MiB (113617276 bytes)
    # download-with: you-get --itag=137 [URL]

Downloading 【ラピスリライツ】LiGHTs「私の名は、光。」特別編集版MV（フルサイズver）.mp4 ...
 100% (108.4/108.4MB) ├████████████████████████████████████████┤[2/2]  162 kB/s
Merging video parts... ffmpeg version 4.2.3 Copyright (c) 2000-2020 the FFmpeg developers
  built with Apple LLVM version 10.0.0 (clang-1000.11.45.5)
  configuration: --prefix=/usr/local/Cellar/ffmpeg/4.2.3 --enable-shared --enable-pthreads --enable-version3 --enable-avresample --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libbluray --enable-libdav1d --enable-libmp3lame --enable-libopus --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librtmp --enable-libspeex --enable-libsoxr --enable-videotoolbox --disable-libjack --disable-indev=jack
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libavresample   4.  0.  0 /  4.  0.  0
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
  libpostproc    55.  5.100 / 55.  5.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from './【ラピスリライツ】LiGHTs「私の名は、光。」特別編集版MV（フルサイズver）[00].mp4':
  Metadata:
    major_brand     : dash
    minor_version   : 0
    compatible_brands: iso6avc1mp41
    creation_time   : 2020-06-12T16:05:32.000000Z
  Duration: 00:04:08.41, start: 0.000000, bitrate: 3529 kb/s
    Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], 32 kb/s, 29.97 fps, 29.97 tbr, 30k tbn, 59.94 tbc (default)
    Metadata:
      creation_time   : 2020-06-12T16:05:32.000000Z
      handler_name    : ISO Media file produced by Google Inc.
Input #1, mov,mp4,m4a,3gp,3g2,mj2, from './【ラピスリライツ】LiGHTs「私の名は、光。」特別編集版MV（フルサイズver）[01].mp4':
  Metadata:
    major_brand     : dash
    minor_version   : 0
    compatible_brands: iso6mp41
    creation_time   : 2020-06-12T16:05:27.000000Z
  Duration: 00:04:08.48, start: 0.000000, bitrate: 129 kb/s
    Stream #1:0(eng): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 5 kb/s (default)
    Metadata:
      creation_time   : 2020-06-12T16:05:27.000000Z
      handler_name    : ISO Media file produced by Google Inc.
Output #0, mp4, to './【ラピスリライツ】LiGHTs「私の名は、光。」特別編集版MV（フルサイズver）.mp4':
  Metadata:
    major_brand     : dash
    minor_version   : 0
    compatible_brands: iso6avc1mp41
    encoder         : Lavf58.29.100
    Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], q=2-31, 32 kb/s, 29.97 fps, 29.97 tbr, 30k tbn, 30k tbc (default)
    Metadata:
      creation_time   : 2020-06-12T16:05:32.000000Z
      handler_name    : ISO Media file produced by Google Inc.
    Stream #0:1(eng): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 5 kb/s (default)
    Metadata:
      creation_time   : 2020-06-12T16:05:27.000000Z
      handler_name    : ISO Media file produced by Google Inc.
Stream mapping:
  Stream #0:0 -> #0:0 (copy)
  Stream #1:0 -> #0:1 (copy)
Press [q] to stop, [?] for help
frame= 7445 fps=0.0 q=-1.0 Lsize=  111075kB time=00:04:08.45 bitrate=3662.4kbits/s speed= 930x
video:106933kB audio:3882kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.233888%
Merged into 【ラピスリライツ】LiGHTs「私の名は、光。」特別編集版MV（フルサイズver）.mp4
```

</details>

<details><summary>点击此处 ← 查看终端</summary>

``` bash
MacPro:Downloads yuangezhizao$ ffmpeg -i 【ラピスリライツ】LiGHTs「私の名は、光 。」特別編集版MV（フルサイズver）.mp4 -vn -acodec copy 私の名は、光。.aac
ffmpeg version 4.2.3 Copyright (c) 2000-2020 the FFmpeg developers
  built with Apple LLVM version 10.0.0 (clang-1000.11.45.5)
  configuration: --prefix=/usr/local/Cellar/ffmpeg/4.2.3 --enable-shared --enable-pthreads --enable-version3 --enable-avresample --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libbluray --enable-libdav1d --enable-libmp3lame --enable-libopus --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librtmp --enable-libspeex --enable-libsoxr --enable-videotoolbox --disable-libjack --disable-indev=jack
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libavresample   4.  0.  0 /  4.  0.  0
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
  libpostproc    55.  5.100 / 55.  5.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from '【ラピスリライツ】LiGHTs「私の名は、光。」特別編集版MV（フルサイズver）.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    encoder         : Lavf58.29.100
  Duration: 00:04:08.48, start: 0.000000, bitrate: 3662 kb/s
    Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(tv, bt709), 1920x1080 [SAR 1:1 DAR 16:9], 3526 kb/s, 29.97 fps, 29.97 tbr, 30k tbn, 59.94 tbc (default)
    Metadata:
      handler_name    : ISO Media file produced by Google Inc.
    Stream #0:1(eng): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 127 kb/s (default)
    Metadata:
      handler_name    : ISO Media file produced by Google Inc.
Output #0, adts, to '私の名は、光。.aac':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    encoder         : Lavf58.29.100
    Stream #0:0(eng): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 127 kb/s (default)
    Metadata:
      handler_name    : ISO Media file produced by Google Inc.
Stream mapping:
  Stream #0:1 -> #0:0 (copy)
Press [q] to stop, [?] for help
size=    3956kB time=00:04:08.45 bitrate= 130.4kbits/s speed=1.44e+03x
video:0kB audio:3882kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 1.884156%
```

</details>

未完待续……