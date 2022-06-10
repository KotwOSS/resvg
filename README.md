```
$$$$$$$\             $$$$$$\  $$\    $$\  $$$$$$\  
$$  __$$\           $$  __$$\ $$ |   $$ |$$  __$$\ 
$$ |  $$ | $$$$$$\  $$ /  \__|$$ |   $$ |$$ /  \__|
$$$$$$$  |$$  __$$\ \$$$$$$\  \$$\  $$  |$$ |$$$$\ 
$$  __$$< $$$$$$$$ | \____$$\  \$$\$$  / $$ |\_$$ |
$$ |  $$ |$$   ____|$$\   $$ |  \$$$  /  $$ |  $$ |
$$ |  $$ |\$$$$$$$\ \$$$$$$  |   \$  /   \$$$$$$  |
\__|  \__| \_______| \______/     \_/     \______/ 
                                                   
Advance your SVG experience
```

![](https://tokei.rs/b1/github/KotwOSS/resvg)
![](https://tokei.rs/b1/github/KotwOSS/resvg?category=blanks)
![](https://tokei.rs/b1/github/KotwOSS/resvg?category=code)
![](https://tokei.rs/b1/github/KotwOSS/resvg?category=comments)
![](https://tokei.rs/b1/github/KotwOSS/resvg?category=files)
<br>

ReSVG is a advanced SVG compiler, which includes many features, and is written in [python](https://www.python.org/).

<hr>
<br>

## License

This project is licensed under the [Mit License](https://mit-license.org/)

<hr>
<br>

# Quick Start

<h2><a href="https://oss.kotw.dev/resvg/INSTALL">Install</a></h2>
<h2><a href="https://oss.kotw.dev/resvg/UNINSTALL">Uninstall</a></h2>
<h2><a href="https://oss.kotw.dev/resvg/USAGE">Usage</a></h2>

<hr>
<br>

## Components

1. [Repeat](examples/repeat/README.md)
   ```xml
   <re:repeat {var}="{exp(int | range | xrange)}" />
   ```
2. [While](examples/while/README.md)
    ```xml
    <re:while cond="{exp(bool)}" />
    ```
3. [If](examples/if/README.md)
    ```xml
    <re:if cond="{exp(bool)}" />
    ```
4. [Lib](examples/lib/README.md)
    ```xml
    <re:lib ns="{raw(str)}" />
    ```
5. [Comp](examples/comp/README.md)
    ```xml
    <re:comp name="{raw(str)}" *args />
    ```
6. [Path](examples/path/README.md)
    ```xml
    <re:path re:transform="{exp(float)};{exp(float)}" *args />
    ```
7. [Include](examples/include/README.md)
    ```xml
    <re:include kup="{raw(str)}" url="{raw(str)}" path="{raw(str)}" />
    ```
8. [Slot](examples/slot/README.md)
    ```xml
    <re:slot/>
    ```
9.  [Run](examples/run/README.md)
    ```xml
    <re:run/>
    ```
<hr>
<br>

If you have aditional ideas how to make this tool better please create a feature request in the issues tab or write me an email at [kekontheworld@gmail.com](mailto:kekontheworld@gmail.com)!

<hr>
<br>

## Contributing

More information [here](https://oss.kotw.dev/resvg/CONTRIBUTE).
