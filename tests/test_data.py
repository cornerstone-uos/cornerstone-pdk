from pathlib import Path

from pdk_data_verifier.cli import validate


def test_pdk_data():
    """Tests the PDK data for completeness and consistency.

    Alternatively, you can run the validation via the terminal with the following command as well:

    `pdk-data-verifier validate .`
    """
    path = Path(".")
    validate(path)
