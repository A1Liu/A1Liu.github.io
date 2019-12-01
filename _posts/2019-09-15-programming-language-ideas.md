---
title: Ideas to Include in a New Programming Language
categories: [programming]
tags: [fun]
---
<!-- {% raw %} -->
<!-- {% include refc-small.html text="ref commit" commit="3cad965..." %} -->
<!-- {% include ref-commit.html text="ref commit" commit="3cad965..." %} -->
<!-- {% endraw %} -->

### Idea: DAG of Programming Language Features
We model the language as a directed, acyclic graph of programming language features,
where each feature is the child of all the features it depends on, or whose behavior
it modifies. Thus, different branches of the graph must be orthogonal, by definition.

##### Application: Disabling Language Features
Language features aren't always a good thing. Sometimes you want dynamic typing,
and other times you want static analysis with type inference. With a DAG of language
features, you can disable features you don't want.

### Idea: Scopes as Anonymous Structs
The namespace of a scope can be accessed as a record (struct without a type name).

##### Application: Immediately-Invoked Lambdas without the Abstraction Cost
Immediately-invoked lambdas are great, but they require the compiler to jump through
lots of hoops. Instead, scopes can be used to emulate the scoping rules of lambdas
without having to do the work of optimizing away the code later.

### Idea: Contracts Over Types/Data Fields
Contracts enforced over data fields in structs, such that each contract must
hold while the struct is valid. Contracts over types would be a special case, where
the type doesn't have fields.

##### Application: Fine-Grained Safety Checks
We can check invariants at compile-time instead of having to check them at runtime,
or while debugging. Additionally, in debug mode we can have runtime checks that
ensure correctness by construction.

### Idea: Associative Scopes
Scopes where the order of execution is explicitly determined at compile-time.
Mutability is not allowed, but initialization after declaration is.

##### Application: Coarse-Grained (i.e. Declarative) Control Flow

### Idea: Loop Invariant Declaration
The programmer declares loop invariants natively in the language.

##### Application: Easier Optimization

### Idea: Orthogonal Pointer Annotations
Pointer annotations for concepts like mutability, ownership, block-type (single object
or array of objects), dispatch-style (dynamic or static), etc.

##### Application: Customizable Safety Checks

### Idea: Compile-Time Source Edits
The compiler is allowed to edit your source during compilation.

##### Application: Cannonicalization Work Can be Saved to Source

### Idea: Language Support for Allocators
Allocators are given the same amount of information that garbage collectors are.

##### Application: Intrusive Allocators

### Idea: Flexible Namespace Captures
Restrict access to a name in the surrounding namespace, or to all but a subsection
of names.

##### Application: Debugging Invariants
Let's say I have a global that, for some reason, doesn't take on the value I
expect it to. With namespace captures, I can simultaneously debug it while also
making my code easier to read. By putting namespace capture restrictions on scopes
in question, I can check, at compile time, which scopes are using the global.
Additionally, I can check exactly which scopes *modify* the global, which is much
harder to do with something simple like text search.

### Idea: Module Permissions
Programmatically prevent modules from doing certain kinds of tasks. For example,
prevent a module from doing anything but computation, as a feature of the language.

##### Application: Secure Black Boxes
If I import a module, I expect it to do what it says on the tin; if it doesn't,
that could be a security vulnerability. I'd like to be able to, at compile time,
check that the module I'm importing doesn't copy my entire file system, compress it,
and post it in a public repo on GitHub.

### Idea: Native Generators
Using an implicitly passed pointer into the stack, we can check whether or not we're
in a generator, and basically keep generator code as straight-line code, instead
of breaking it up into separate pieces first.

Here's how it would work:
-  Generator code is called with a pointer into the call stack where they were called.
   When you run the generator, it yields typed objects, along with a pointer into
   the binary saying which instruction it was on.
-  Generator code that doesn't yield a value or have no more values to yield will return
   a null pointer instead. Additionally, when the generator code is called with
   a null pointer, then it goes to its return value and skips any remaining yields.
-  Generators themselves are just objects on the stack that are copied in and out
   of the heap as needed. The first field is always the pointer into the callstack.
-  An advantage of this style is that any arbitrary function can be trivially turned
   into a generator by just adding read barriers in the original function and
   adding a pointer

### Idea: Garbage Collector API
Have an API which the program can use to communicate with the garbage collector
at runtime.

##### Application: Deterministic Tracing Collector
If the program is able to communicate with the garbage collector, mark and sweep
collectors can be deterministically run.

##### Deterministic Destruction in GC'd Languages
With a GC API, programs can manually invalidate references to objects, and thus
deterministic destruction of resources, like what C++ and Rust have, can be done
in a GC'd language like Java. On instantiation, the program can tie a specific
reference's lifetime to the lifetime of the object, and force the GC to do a collection
of that object when the reference goes out of scope. Then, the GC can deterministically
destruct objects during that forced collection.

### Idea: Macro Objects
Objects that are destructured into their comonent parts, and whose methods get
inlined automatically. They're objects during type checking, but then are
expanded type-safely during compilation.

Macro objects have a few notable downsides:
-  Because their methods are always inlined, recursion is not allowed.
-  They have no defined structure at runtime, so things like the `sizeof` function
   won't work on them
-  They can only be passed as compile-time parameters to functions that expect
   macro objects.

##### Application: RAII without the Overhead
RAII can be done without any compile-time or runtime overhead, by just inlining
the necessary statements.

##### Application: High-level State Transitions
We can use objects to manage state transitions, without actually creating any
objects. Things like application state transitions can be done with a state manager
in global scope, but without having actual objects being constructed.

##### Application: Complex Iterators without the Overhead
The following code in Rust:

```rust
return vec.windows(2).map(|w| w[0] + w[1])
```

should trivially boil down to this:

```rust
let new_vec = Vec::with_capacity(vec.len() - 1);
for i in 0..(vec.len() - 1) {
    new_vec.push(vec[i] + vec[i + 1]);
}
return new_vec;
```

The problem is that the original code uses struct definitions, which the compiler
doesn't know are intended to be optimized out later. If all their definitions were
inlined automatically, the above transformation could be done in debug mode, with
nice error messages when things don't work out, and wouldn't requre any heavy duty
optimization.

### Idea: Constructor Function-Call Restrictions
Since the body of every constructor by definitly has access to uninitialized state,
using functions/methods in a constructor can be dangerous. Thus, calling code should
be limited to instances where the code understands that the object has not been
initialized yet. So for example, a function that's called in a constructor must
declare that it's ok with an unitialized instance of an object.

##### Application: Actual Null Safety
In "null-safe" languages like Kotlin, null pointer exceptions are still possible
when calling a function in a constructor. Restricting the functions that can be
called in a constructor would remove this exception to the rule.
