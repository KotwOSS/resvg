# Usage

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

Only display the errors:

```sh
resvg --compile --only-errors -i input.rsvg
```

Pretty print the xml:

```sh
resvg --compile --pretty -i input.rsvg
```

Trust statements:

```sh
resvg --trust-stmt
```

Trust expressions:

```sh
resvg --trust-exp
```

Trust expressions and statements:

```sh
resvg --trust
```

Hide the logo:

```sh
resvg --hide-logo
```

Specify the newline character:

```sh
resvg --newl "\n"
```

Specify the indent space count:

```sh
resvg --indent 4
```

Keep the comments:

```sh
resvg --comments
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
