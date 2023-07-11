"""
csproj file parsing tests
"""

import xml.etree.ElementTree as ET
import tempfile
import os

import pytest
import xml_utils as xml

@pytest.fixture
def create_test_csproj_file(request):
    """
    Create a csproj file with the given package references
    """
    root = ET.Element('Project')
    item_group_element = ET.SubElement(root, 'ItemGroup')
    for name, version in request.param.items():
        package_reference_element = ET.SubElement(item_group_element, 'PackageReference')
        package_reference_element.set('Include', name)
        package_reference_element.set('Version', version)

    temp_file = tempfile.NamedTemporaryFile(delete=False)

    tree = ET.ElementTree(root)
    tree.write(temp_file.name)

    yield temp_file.name
    os.unlink(temp_file.name)

@pytest.mark.parametrize('create_test_csproj_file', [{'Newtonsoft.Json': '12.0.3'}], indirect=True)
def test_find_package_references_single_package(create_test_csproj_file):
    file_path = create_test_csproj_file
    package_references = xml.find_package_references(file_path, 'Newtonsoft.Json')
    assert len(package_references) == 1
    assert package_references[0].get('Version') == '12.0.3'

@pytest.mark.parametrize('create_test_csproj_file', [
    {'Newtonsoft.Json': '12.0.3', 'Microsoft.Extensions.Logging': '5.0.0'}
    ], indirect=True)
def test_find_package_references_multiple_packages(create_test_csproj_file):
    file_path = create_test_csproj_file
    package_references = xml.find_package_references(file_path, 'Microsoft.Extensions.Logging')
    assert len(package_references) == 1
    assert package_references[0].get('Version') == '5.0.0'

@pytest.mark.parametrize('create_test_csproj_file', [
    {'Newtonsoft.Json': '12.0.3', 'Microsoft.Extensions.Logging': '5.0.0'}
    ], indirect=True)
def test_find_package_references_no_packages(create_test_csproj_file):
    file_path = create_test_csproj_file
    package_references = xml.find_package_references(file_path, 'Any.Package')
    assert len(package_references) == 0
