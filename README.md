# Installation

Include this package as dependency in your project.

```bash
uv add git+https://github.com/profanta3/eimer_client
```

When this code has changed, update your local dependency with:

```bash
uv sync --upgrade
```


# Notes for the server

```
Ring numbers for moves:
    0(1(2(3(4)3)2)1)0
    0 is out of bounds
taken into account in send data to act like this:
    (0(1(2(3)2)1)0)

Moves encoded after testing:

        |Move        
Send    |From   |To     |Note
5       |3      |2      |Illegal (Server States -3 to -2)
6       |2      |1      |Works (Server States -2 to -1)
7       |1      |0      |Works (Server States -1 to 0)
8       |0      |1      |Works
9       |1      |2      |Works
10      |2      |3      |Works
```