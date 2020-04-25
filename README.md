# quasicode

Programming as it should be.

``` bash
$ qc run examples/hello-world.qc
hello world
```

What Is Implemented? | What Doesn't 'Work'?
---|---
endless loops, breaking | `qc` does not prioritize mathematical operators. This is not a bug but rather a feature.
variable assignment, computing with the standard math operators `+`, `-`, `*`, `/`, `modulo`™ | There are no comments. If your code doesn't comment itself, you're doing it wrong.
function declaration | 

## Installing

``` bash
git clone https://github.com/witling/quasicode

cd quasicode
chmod +x install

./install
```

## How To Use

Usage | `qc` Keyword | Description | Example
---|---|---|---
print | `quasi <value>` | put a value to stdout | `quasi "gut"`
true, false | `uzbl`, `not uzbl` | truth values | `vim ist not uzbl`
operators | `+`, `-`, `*`, `/`, `modulo`, `<` | mutate values | `quasi (1 + 1)`
logical operators | `<value> das ist <value>` | compare two values | `0 das ist 0`
if | `kris?` | ask kris. he has all the answers | `kris? a das ist b`
else if | `kris??` | if he didn't know first, he'll know now | `kris?? i modulo 10 das ist 0`
else | `ach kris.` | give up |
loop | `das holen wir nach` | for real |
break | `patrick!` | break out of a loop |
assignment | `<ident> ist <value>`, `<value> also <ident>` | set a variable to a given value | `vim ist 1`, `3 also pi`
return | `<value> und fertig` | set the return value of a function | `42 und fertig`
function declaration | `und zwar <ident> (mit <arg1> <arg2>) (action please)` | declare a function. `action please` marks the program entry point | `und zwar main action please`
breakpoint | `hä` | open pudb to debug the interpreter | `hä`
speed up | `so` |  | `so`

## How To Extend

Quasicode heavily relies on Python functionality. To implement a new library, create a Python class that inherits from `qclib.library.PyLibrary`.

There are some quirks to fix when implementing libraries. This is mainly due to the way libraries are serialized. **Note:**

- The classes `__module__` should be set to `__main__`.
- Also, don't use `super()` to address the parent class but rather write the name out e.g. `super().__init__()` becomes `PyLibrary.__init__(self)`.
- Function-local `import` does not work. Import everything at the top of the file.
- All functions must be subject to the library class.

### Development

use this to format code before committing:

```
yapf --recursive .
```
