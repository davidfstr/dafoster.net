---
layout: post
title: Notes on Prolog
tags: [Software]

---

## What is Prolog?

Prolog is a declarative programming language that, given a list of axioms and a list of implication rules, can deduce the truth (or falsehood) of a logical statement.

For example, given the following knowledge base (AKA *database*):

<pre>
% Axiom: Mary likes Ted.
likes(mary,ted).
% Axiom: Jane likes Ted.
likes(jane,ted).
% Rule: X is jealous of Y if they both like Z (and are not the same person).
jealous(X,Y) :- likes(X,Z), likes(Y,Z), X \= Y.
</pre>

I can ask the question `jealous(mary,jane)` and get the affirmation `true`.
Or I can ask the question `jealous(mary,mary)` and get the denial `false`.[^period-question]

I can also ask a more complicated question containing variables and Prolog will derive the possible values (and relations) the variables must have in order to make the question posed to be true.

For example, asking the question `jealous(X,Y)` will give the results:

<pre>
X = mary,
Y = jane ;
X = jane,
Y = mary
</pre>

As another (more interesting) example, consider the knowledge base:

<pre>
% Rule: A line is horizontal if its points have the same Y coordinate.
horizontal(line( point(_,Y), point(_,Y) )).
% Rule: A line is vertical if its points have the same X coordinate.
vertical(line( point(X,_), point(X,_) )).
</pre>

And the questions:

<pre>
(1) horizontal(line( point(0,0), point(X,Y) )).  ==>  Y = 0.
(2) horizontal(line( point(0,0), P2 )).          ==>  P2 = point(_G327, 0).
</pre>

The second question is particularly interesting because it gave back a fairly complicated answer: `P2` must be a `point`, its X coordinate can be anything, but its Y coordinate must be zero. I think it's particularly cool that Prolog can deduce that P2 must be a point. <!-- LPN §2.1 -->

As a final example of a simple problem solvable by Prolog, consider the [crossword puzzle] in Exercise 2.4 of "Learn Prolog Now!". You can write a Prolog program to solve crossword puzzles!

[^period-question]: When posing a question in the Prolog interpreter, you must include a trailing period at the end of the question.

[crossword puzzle]: http://www.learnprolognow.org/lpnpage.php?pagetype=html&pageid=lpn-htmlse7


## When is Prolog useful?

Prolog's deduction capabilities makes it useful for answering questions and making deductions within systems whose concepts can be expressed in a formal hierarchy. <!-- LPN §2.1 -->

In academia, for example, Prolog has been used to investigate natural language formalizations and expert systems in artificial intelligence. <!-- LPN §2.1 -->

### Case Study: Java bytecode verifier

As a more practical example, Prolog has also been used to define the semantics of the Java bytecode verifier[^java-verifier] for Java 6.[^cite-java-prolog] Prior versions of Java had a verifier whose semantics were defined by a textual specification only (namely the Java Virtual Machine Specification).

There are a few advantages to having the verifier defined in terms of Prolog:

* The specification becomes formal (and thereby unambiguous and more likely to be error-free).
* The execution model for performing the verification becomes well-defined (since it would use Prolog's) and fast (since Prolog's core unification algorithm is fast<!-- LPN §2.1 -->).

[^java-verifier]: The job of the Java bytecode verifier is to examine a compiled Java program and check whether it is well-structured and therefore (reasonably) safe for the Java virtual machine to execute. For example the verifier would reject a Java program containing a command to jump to an instruction location outside of the current method.

[^cite-java-prolog]: See the [Java Virtual Machine Specification](http://docs.oracle.com/javase/specs/jvms/se7/html/index.html). Particularly "Preface to the Java SE 7 Edition" and §4.10 "Verification of class Files".


## Writing Programs

### Functions as Rules

So how do you actually write something resembling a *program* in Prolog? Until now we've been talking about axioms, rules, and questions. But in most languages a program consists of a series of expressions that are evaluated.

For example in Python, you might write:

<pre>
def add(x, y):
    return x + y

print add(5, 3)    # prints 8
</pre>

In Prolog, you can do something similar by defining a rule where one of the variables in the rule (typically the last one) is its "output":

<pre>
add(X, Y, Result) :- Result is X + Y.
</pre>

To actually evaluate this "function" with 5 and 3 you would ask the question `add(5, 3, Result)` which would yield `Result = 8`.

Now, don't get trapped into the idea that such as rule always needs to be evaluated in one direction. In Prolog you have the additional power to ask what the "inputs" of the function has to be to yield an already-known "output".

For example, you could ask the question `add(X, 3, 8)` to deduce that "input" X must be 5.[^is-problems] You could even try asking `add(X, Y, 8)` to find all values of X and Y that yield 8 as a result (although there are an infinite number of such combinations in this example).[^collecting-solutions]

This power to flip functions on their head is a unique quality of Prolog. (And it blows my mind.)

Ultimately a rule specifies a set of relationships between its arguments. Thus arguments can be "inputs", "outputs", or even temporary variables (like accumulators).

[^is-problems]: Unfortunately the `is` clause in this example cannot be run "backwards", so this particular question will fail. (I am not sure why this particular restriction on `is` exists.)

[^collecting-solutions]: A Prolog *program* that wanted to collect all combinations of inputs in this fashion (as opposed to a user at the interpreter) would probably use a combination of the `findall`, `bagof`, and `setof` special rules. See [LPN §11.2 "Collecting Solutions"](http://www.learnprolognow.org/lpnpage.php?pagetype=html&pageid=lpn-htmlse49) for more information.

### Processing Recursive Data Structures

Processing recursive data structures such as lists and trees is mind bending... For examples see:

* [LPN §6.1 "Append"] and
* [LPN §6.2 "Reversing a List"].

[LPN §6.1 "Append"]: http://www.learnprolognow.org/lpnpage.php?pagetype=html&pageid=lpn-htmlse24
[LPN §6.2 "Reversing a List"]: http://www.learnprolognow.org/lpnpage.php?pagetype=html&pageid=lpn-htmlse25


## Interactive Use (as a REPL)

It is possible to run Prolog in an interactive fashion by using the `assert` special rule at runtime to define new statements (i.e. axioms and rules). And `listing` will display the set of statements that have been defined. Finally `retract` and `retractall` can be used to undefine statements.

These special rules, however, are not restricted to use in the interpreter - they can also be used at runtime by rules in programs. For example memoization[^memo] is a good use for dynamic calls to `assert`.

[LPN §2.2 "Proof Search"]: http://www.learnprolognow.org/lpnpage.php?pagetype=html&pageid=lpn-htmlse6
[LPN §2.4 "Practical Session"]: http://www.learnprolognow.org/lpnpage.php?pagetype=html&pageid=lpn-htmlse8

[^memo]: Memoization is where a function that computes a value caches the result of the computation so that repeated invocations with the same input can immediately return the saved result. This can speed of performance in certain applications. See [LPM §11.1 "Database Manipulation"](http://www.learnprolognow.org/lpnpage.php?pagetype=html&pageid=lpn-htmlse48) for an example.


## Question Evaluation <small>(Unification, Backtracking)</small>

When evaluating a question, Prolog takes the question expression and matches it against the axioms and rules in the input knowledge base. The algorithm used for matching is called *unification*. While performing unification, Prolog makes guesses about what values should be assigned to each variable in the question expression. If it encounters a contradiction, it *backtracks* to one of its previous guesses and revises the guess. This process is described graphically in [LPN §2.2 "Proof Search"].

Although Prolog is a declarative language, the precise behavior of evaluating queries depends on the order that rules and clauses are defined. In particular the performance of the same program can vary significantly depending on ordering. As another gotcha, if you define rules in a left-recursive fashion (as opposed to a right-recursive one), Prolog will go into an infinite loop when evaluating the rule.

It is possible to debug (and step through) the evaluation of a question expression using the **trace** command, which is described in [LPN §2.4 "Practical Session"]. This is useful for investigating performance issues.

### Cuts

It is possible to optimize the execution of a Prolog rule by adding a **cut** as a clause. This is written as a bang (`!`). Unfortunately to use cuts effectively (and correctly), you have to understand the exact execution model used by Prolog. It is quite easy to unwittingly insert a cut that actually changes the semantics of the original rule. <!-- LPN §10.1, §10.2 -->

There are even hacks you can do with cuts such as implementing "negation as failure" (`\+`). But again you have to be very careful since cuts can change your knowledge base's semantics. <!-- LPN §10.3 -->


## Side Effects & I/O

Some built-in clauses trigger side effects when they are examined by the unification algorithm. Programs take advantage of such "impure predicates" to do I/O and other types of side-effecting work.

For example asking the question `print('Hello')` will print `Hello` to the screen.[^str-symbol]

To write to a file you might define:

<pre>
printfile(Filename, Text) :-
    open(Filename, write, Stream),
    write(Stream, Text), nl(Stream),
    close(Stream).
</pre>

And then pose the question `printfile('hogwarts.txt', 'Hogwarts')`.

During evaluation, the `printfile` is rewritten to `open(...) AND write(...) AND nl(...) AND close(...)`. Each of those subclauses is then each evaluated to `true` (performing the associated side effect) and the overall clause becomes just `true`.

[^str-symbol]: Note that `'Hello'` (with single quotes) is a variable, not a string. The string `"Hello"` (with double quotes) is equivalent to a list of codepoints (`[72, 101, 108, 108, 111]`).


### *References*

* LPN: [Learn Prolog Now!](http://www.learnprolognow.org/lpnpage.php?pageid=online)


### *Related Articles*

* [Unique Features of Various Programming Languages](/articles/2013/01/29/unique-features-of-various-programming-languages/)
    * *Describes several other programming languages and their unique features.*
