# NuGet references scanner

This Python script searches for a specified NuGet package within .NET project repositories located in a specified root folder. It finds and prints the version of the specified package.

## Installation

This script requires Python 3.10 or newer. You can install the required libraries with:

```bash
pipenv install
```

## Usage

To use this script, you can run it from your terminal with various options.

* `--root-folder`: Specifies the root folder containing .NET project repositories.
* `--package-name`: Specifies the NuGet package name to search for.
* `--mode`: Specifies the resolving dependencies mode, which can be "direct" or "transitive".
* `--update-git`: If specified, updates git repositories before searching. Only in this case the folders have to be git repositories.
* `--format-md`: If specified, outputs results in markdown format. If not specified, outputs in text format.

For example, to find versions of a package named `Package1` in solutions folder named `MyDotnetProjects`, you might run:
```bash
python main.py --root-folder MyDotnetProjects --package-name Package1 --mode direct
```

## Prerequisites

This script requires Python 3.10 or newer. If using transitive mode, it also requires [dotnet](https://dotnet.microsoft.com/en-us/download/dotnet) to be installed.

## Tests

You can run tests with:
```bash
pipenv run pytest
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## License

[MIT](LICENSE.md)