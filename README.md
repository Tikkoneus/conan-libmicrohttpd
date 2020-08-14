
# conan-libmicrohttpd

[Conan.io](https://conan.io) package for libmicrohttpd library

The packages generated with this **conanfile** can be found in [bintray.com](https://conan.io/source/DEGoodmanWilson/0.9.51/DEGoodmanWilson/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py
    
## Upload packages to server

    $ conan upload libmicrohttpd/0.9.51@DEGoodmanWilson/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install libmicrohttpd/0.9.51@DEGoodmanWilson/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    libmicrohttpd/0.9.51@DEGoodmanWilson/stable

    [options]
    libmicrohttpd:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
