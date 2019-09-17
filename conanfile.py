#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class HiredisConan(ConanFile):
    name = "hiredis"
    version = "0.14.0"
    description = "Minimalistic C client for Redis >= 1.2"
    topics = ("conan", "nng", "communication", "messaging", "protocols")
    url = "https://github.com/zinnion/conan-hiredis"
    homepage = "https://github.com/redis/hiredis"
    author = "Zinnion <mauro@zinnion.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    short_paths = True
    generators = "cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    options = {
       "shared": [True, False],
    }

    default_options = (
        "shared=False"
    )

    def source(self):
        self.run("git clone https://github.com/redis/hiredis.git source_subfolder")

    def configure(self):
        del self.settings.compiler.libcxx

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(src=self.source_subfolder, pattern="*.h", dst="include", keep_path=False)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
