#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import subprocess


class LibmicrohttpdConan(ConanFile):
    name = "libmicrohttpd"
    version = "0.9.71"
    url = "http://github.com/DEGoodmanWilson/conan-libmicrohttpd"
    description = "A small C library that is supposed to make it easy to run an HTTP server as part of another application."
    license = "https://www.gnu.org/software/libmicrohttpd/manual/html_node/GNU_002dLGPL.html"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False],
               "disable_https": [True, False],
               "disable_messages": [True, False],
               "disable_postprocessor": [True, False],
               "disable_dauth": [True, False],
               "disable_epoll": [True, False]}
               #TODO add in non-binary flags
    default_options = "shared=False",\
                      "disable_https=True",\
                      "disable_messages=False",\
                      "disable_postprocessor=False",\
                      "disable_dauth=False",\
                      "disable_epoll=False"

    def source(self):
        zip_name = "{0}-{1}.tar.gz".format(self.name, self.version)
        tools.download("http://ftp.gnu.org/gnu/{0}/{1}".format(self.name, zip_name), zip_name)
        tools.untargz(zip_name)

        extracted_dir = "{0}-{1}".format(self.name, self.version)
        os.rename(extracted_dir, "sources")

    def configure(self):
        # Because this is pure C
        del self.settings.compiler.libcxx

        if not self.options.disable_https:
            self.requires.add("gnutls/3.6.2@DEGoodmanWilson/stable", private=False)
            self.requires.add("libgcrypt/1.7.3@DEGoodmanWilson/stable", private=False)


    def build(self):

        with tools.chdir("sources"):

            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = True
            env_build.libs.append("pthread")


            config_args = []

            # add gnutls and gcrypt install paths
            if not self.options.disable_https:
                for path in self.deps_cpp_info.lib_paths:
                    if "libgcrypt" in path:
                        config_args.append("--with-libgcrypt-prefix={0}".format('/lib'.join(path.split("/lib")[0:-1]))) #remove the final /lib. There are probably better ways to do this.
                    if "gnutls" in path:
                        config_args.append("--with-gnutls={0}".format('/lib'.join(path.split("/lib")[0:-1]))) #remove the final /lib. There are probably better ways to do this.

            # add user options
            for option_name in self.options.values.fields:
                if(option_name == "shared"):
                    if(getattr(self.options, "shared")):
                        config_args.append("--enable-shared")
                        config_args.append("--disable-static")
                    else:
                        config_args.append("--enable-static")
                        config_args.append("--disable-shared")
                else:
                    activated = getattr(self.options, option_name)
                    if activated:
                        self.output.info("Activated option! %s" % option_name)
                        config_args.append("--%s" % option_name)

            config_args.append("--enable-messages")

            # This is a terrible hack to make cross-compiling on Travis work
            if (self.settings.arch=='x86' and self.settings.os=='Linux'):
                env_build.configure(args=config_args, host="i686-linux-gnu") #because Conan insists on setting this to i686-linux-gnueabi, which smashes gpg-error hard
            else:
                env_build.configure(args=config_args)
            env_build.make()

    def package(self):
        self.copy(pattern="COPYING*", src="sources")
        self.copy("*.h", "include", "sources/src/include", keep_path=True)
        # self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="sources/src/microhttpd/.libs", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="sources/src/microhttpd/.libs", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="sources/src/microhttpd/.libs", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="sources/src/microhttpd/.libs", keep_path=False)

        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if not self.settings.os == "Windows":
            self.cpp_info.cppflags = ["-pthread"]



