# quasicode

Programming as it should be.

``` bash
$ qc run examples/hello-world.qc
hello world
```

## Installing

``` bash
git clone https://github.com/witling/quasicode

cd quasicode
chmod +x install

./install
```

We have a [vim plugin](https://github.com/witling/quasi.vim) for syntax support. What else do you really need?

## How To Use

Have a look at the [Cheatsheet](./CHEATSHEET.md) on how to use and extend quasicode. 

### Development

What Is Implemented? | What Doesn't 'Work'?
---|---
endless loops, breaking | `qc` does not prioritize mathematical operators. This is not a bug but rather a feature.
variable assignment, computing with the standard math operators `+`, `-`, `*`, `/`, `modulo`™ | There are no comments. If your code doesn't comment itself, you're doing it wrong.
function declaration | 

Use this to format code before committing:

```
yapf --recursive .
```
