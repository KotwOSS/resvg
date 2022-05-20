```
░█▀▀█ █▀▀ ░█▀▀▀█ ░█  ░█ ░█▀▀█ 
░█▄▄▀ █▀▀  ▀▀▀▄▄  ░█░█  ░█ ▄▄ 
░█ ░█ ▀▀▀ ░█▄▄▄█   ▀▄▀  ░█▄▄█
Advance your SVG experience
```
![](https://tokei.rs/b1/github/KotwOSS/resvg)
![](https://tokei.rs/b1/github/KotwOSS/resvg?category=blanks)
![](https://tokei.rs/b1/github/KotwOSS/resvg?category=code)
![](https://tokei.rs/b1/github/KotwOSS/resvg?category=comments)
![](https://tokei.rs/b1/github/KotwOSS/resvg?category=files)
<br>

ReSVG is a advanced SVG compiler which includes many features which is written in [python](https://www.python.org/).

<br>

## License
This project is licensed under the [Mit License](https://mit-license.org/)

<hr>
<br>

## Features

1. [Loops](examples/repeat/doc.md)
2. [Conditions](examples/if/doc.md)
3. [Variables](examples/define/doc.md)

<hr>
<br>

## Installation

Linux:
```bash
git clone https://github.com/KotwOSS/resvg.git
cd resvg
chmod +x resvg.py
sudo ln resvg.py /usr/bin/resvg
```

<hr>
<br>

## Usage

Show the help:
```sh
resvg --help
```

Show the version:
```sh
resvg --version
```

Compile a ReSVG file to a SVG file:
```sh
resvg --compile -i input.rsvg -o output.svg
```

Compile a ReSVG file and print it inside of the terminal:
```sh
resvg --compile -i input.rsvg
```

Silent mode:
```sh
resvg --silent
```

Log to a file:
```sh
resvg --log myfile.log
```

Specify the logging level:
```sh
resvg --level [-1-3]
```

**Log Levels**<br>
-1: Debug<br>
0: Info<br>
1: Warning<br>
2: Error<br>
3: Fatal<br>

<hr>
<br>

If you have aditional ideas how to make this tool better please create a feature request in the issues tab or write me an email at [kekontheworld@gmail.com](mailto:kekontheworld@gmail.com)!

<hr>
<br>

## Contributing
More information [here](https://oss.kotw.dev/resvg/CONTRIBUTE).
