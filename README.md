# quasicode

Programming as it should be.

``` bash
$ python3 qc examples/hello-world.qc
"helloworld"
```

## How To Use

Usage | `qc` Keyword | Description | Example
---|---|---|---
print | `quasi <value>` | put a value to stdout |
truth values | `uzbl`, `not uzbl` |  | `vim ist not uzbl`
operators | `+`, `-`, `*`, `/`, `modulo` | | `quasi (1 + 1)`
if | `kris?` | ask kris. he has all the answers | `kris?`
else if | `kris??` | if he didn't know first, he'll know now |
loop | `das holen wir nach` | for real |
break | `patrick!` | |
assignment | `<ident> ist <value>`, `<value> also <ident>` | |
return | `<value> und fertig` | set the return value of a function | `42 und fertig`
function declaration | `und zwar <ident> (mit <arg1> <arg2>) (action please)` |  | `und zwar main action please`
speed up | `so` |  | `so`

## What Is Implemented?

- endless loops, breaking
- variable assignment, computing with the standard math operators `+`, `-`, `*`, `/`, `modulo`™
- function declaration (without parameters)

## What Doesn't 'Work'?

- `qc` does not prioritize mathematical operators. This is not a bug but rather a feature.
- strings are not parsed correctly. just don't use spaces inside them, okey?
- empty lines lead to parsing errors. actually, this is a feature as well as it saves disk space.
- parantheses are not supported (yet?)
