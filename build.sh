build_libgbemu()
{
    pushd libgbemu

    make TOOLCHAIN=$1 LIB_SUFFIX=$2
    mv -f libgbemu-$2 ../renpy-project/game/libgbemu/

    popd
}

TOOLCHAIN=
LIB_SUFFIX= 

case $1 in
    "windows")
        TOOLCHAIN=i686-w64-mingw32-
        LIB_SUFFIX=windows-x86_64.dll
        ;;
    "linux")
        TOOLCHAIN=
        LIB_SUFFIX=linux-x86_64.so
        ;;
    "mac")
        TOOLCHAIN=
        LIB_SUFFIX=mac-x86_64.dylib
        ;;
    *)
        exit
        ;;
esac

build_libgbemu "$TOOLCHAIN" "$LIB_SUFFIX"