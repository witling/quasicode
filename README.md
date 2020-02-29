# quasicode

Programming as it should be.

``` bash
$ python3 qc examples/hello-world.qc
hello world
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

## What Is Implemented?

- endless loops, breaking
- variable assignment, computing with the standard math operators `+`, `-`, `*`, `/`, `modulo`™
- function declaration

## What Doesn't 'Work'?

- `qc` does not prioritize mathematical operators. This is not a bug but rather a feature.

### Development

use this to format code before committing:

```
yapf --recursive .
```
