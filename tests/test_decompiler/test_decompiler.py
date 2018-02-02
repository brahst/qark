import os
import shutil

import pytest

from qark.decompiler import decompiler
from qark.decompiler.external_decompiler import JDCore, CFR, Procyon


def test_download_apktool():
    if os.path.exists(decompiler.APK_TOOL_PATH):
        shutil.rmtree(decompiler.APK_TOOL_PATH)
    assert not os.path.exists(decompiler.APK_TOOL_PATH)
    decompiler.download_apktool()

    assert os.path.exists(decompiler.APK_TOOL_PATH)
    shutil.rmtree(decompiler.APK_TOOL_PATH)
    assert not os.path.exists(decompiler.APK_TOOL_PATH)


def test_download_dex2jar():
    if os.path.exists(decompiler.DEX2JAR_PATH):
        shutil.rmtree(decompiler.DEX2JAR_PATH)
    assert not os.path.exists(decompiler.DEX2JAR_PATH)
    decompiler.download_dex2jar()

    assert os.path.exists(decompiler.DEX2JAR_PATH)
    shutil.rmtree(decompiler.DEX2JAR_PATH)
    assert not os.path.exists(decompiler.DEX2JAR_PATH)


def test_download_cfr(cfr_path):
    if os.path.isfile(cfr_path):
        os.remove(cfr_path)
    assert not os.path.isfile(cfr_path)
    decompiler.download_cfr()

    assert os.path.isfile(cfr_path)
    os.remove(cfr_path)
    assert not os.path.isfile(cfr_path)


def test_download_procyon(procyon_path):
    if os.path.isfile(procyon_path):
        os.remove(procyon_path)
    assert not os.path.isfile(procyon_path)
    decompiler.download_procyon()

    assert os.path.isfile(procyon_path)
    os.remove(procyon_path)
    assert not os.path.isfile(procyon_path)


def test_unzip_file(path_to_source, build_directory):
    decompiler.unzip_file(path_to_source, destination_to_unzip=build_directory)

    with pytest.raises(SystemExit):
        decompiler.unzip_file("1")

    shutil.rmtree(build_directory)
    assert not os.path.isdir(build_directory)


def test_get_java_version():
    java_version = decompiler.get_java_version()
    assert not java_version.startswith('"')
    assert not java_version.endswith('"')


def test_ran_unpack_apk(decompiler):
    classes_dex_path = os.path.join(decompiler.build_directory, "classes.dex")
    assert classes_dex_path == decompiler.dex_path
    assert os.path.isfile(classes_dex_path)

    shutil.rmtree(decompiler.build_directory)
    assert not os.path.isdir(decompiler.build_directory)


def test_ran_apktool(decompiler):
    assert os.path.isfile(os.path.join(decompiler.build_directory, "AndroidManifest.xml"))

    shutil.rmtree(decompiler.build_directory)
    assert not os.path.isdir(decompiler.build_directory)


def test_ran_dex2jar(decompiler):
    assert os.path.isfile(decompiler.jar_path)
    assert decompiler.jar_path.endswith(".jar")

    shutil.rmtree(decompiler.build_directory)
    assert not os.path.isdir(decompiler.build_directory)


def test_decompile(decompiler):
    jdcore_decomp_path = os.path.join(decompiler.build_directory, "jdcore")
    procyon_decomp_path = os.path.join(decompiler.build_directory, "procyon")
    cfr_decomp_path = os.path.join(decompiler.build_directory, "cfr")
    assert all([not os.path.exists(path) for path in (jdcore_decomp_path, procyon_decomp_path, cfr_decomp_path)])

    decompiler.decompile()

    assert os.path.isdir(decompiler.build_directory)

    assert os.path.isdir(jdcore_decomp_path)
    assert os.path.isdir(os.path.join(jdcore_decomp_path, "org"))

    assert os.path.isdir(procyon_decomp_path)
    assert os.path.isdir(os.path.join(procyon_decomp_path, "org"))

    assert os.path.isdir(cfr_decomp_path)
    assert os.path.isdir(os.path.join(cfr_decomp_path, "org"))

    shutil.rmtree(decompiler.build_directory)
    assert not os.path.isdir(decompiler.build_directory)


@pytest.mark.parametrize("external_decompiler", [
    (JDCore()),
    (CFR()),
    (Procyon()),
])
def test_decompiler_function(decompiler, external_decompiler):
    decompiler._decompiler_function(external_decompiler)
    decompiler_build_directory = os.path.join(decompiler.build_directory, external_decompiler.name)
    assert os.path.isdir(decompiler_build_directory)
    assert os.path.isdir(os.path.join(decompiler_build_directory, "org"))
    shutil.rmtree(decompiler.build_directory)
    assert not os.path.isdir(decompiler.build_directory)
