[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9447068&assignment_repo_type=AssignmentRepo)
# Project 5: Simulating transposable elements

In the last project, we imagine that someone has hired us to help out with simulating a genome containing [transposable elements]. (I know people who has such strange interests, so it is not beyond the realm of possibilities).

We won’t do anything complicated, this is just an exercise after all, but we will want to simulate TEs as stretches of DNA that can copy themselves elsewhere in the genome.

Our employer already has most of the simulator up and running. She has a program that randomly picks operations to do—insert a TE ab initio, copy a TE, or disable one with a mutation—but she needs us to program a representation of a genome to track where the TEs are.

There are multiple ways to do this, but you should implement at least two: one based Python lists, where each nucleotide is represented by one entry in a list, and one based on linked lists, where each nucleotide is represented by a link. If you feel ambitious, you can try others (for example keeping track of ranges of a genome with the same annotation so you don’t need to explicitly represent each nucleotide).

## Genome interface

A genome should be represented as a class that implements the following methods:

```python
class Genome(ABC):
    """Representation of a circular enome."""

    def __init__(self, n: int):
        """Create a genome of size n."""
        ...  # not implemented yet

    @abstractmethod
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # not implemented yet

    @abstractmethod
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # not implemented yet

    @abstractmethod
    def __len__(self) -> int:
        """Get the current length of the genome."""
        ...  # not implemented yet

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet

```

The `ABC` and `@abstractmethod` just means that this class is not something you can use by itself, but that another class must implement the details. In `src/genome.py` you will find templates for a Python list tand a linked list implementation (without the actual implementation, because you have to implement them).

You are free to implement the genome classes however you want, and using whateer auxilary data structures you desire, as long as one uses a Python list with an element for each nucleotide and the other a linked list with a link for each nucleotide. If you want to implement a third (or fourth or fifth...) version, you are very welcome to do so as well.

## Complexity

When you have implemented the two (or more) classes, describe the complexity of each operation as a function of the genome size (at the time of the operation), and the size of the TE involved (and when copying, the offset you are copying). Put the description here:

**Operation Complexity**

n is the size of the genome
m is the TE size
l is the offset
p is the number of active TE

n > p, there can never be more active TE's than the length of the genome.

### List Genome

#### init

init has a complexity of O(n).

self.genome creates a list of length n in in time O(n), and is the most complex operation in the function.

#### insert_te

insert_te has a complecity of O(m*n)

The most complex operation in the inser_te function is self.genome[pos:pos] = te. This has to insert the entire TE, moving every element after it by the length of the genome. Worst case would be inserting the TE at position 0, inserting m elements at zero (O(m)) and then pushing n elements by m (O(m*n)). Compared to this complexity, the key loop (O(p)) and the **pos < start** loop (O(p)) do not seem relevant. When a TE is inserted at 0, the **pos < start** loop has a max run-time of O(p) because every start position of every active TE must be updates. The **start < pos <= end** loop should evaluate p times, but only run once, as a new TE can only knock-out 1 other TE, giving it the O(p) complexity.

#### copy_te

copy_te has a complexity of O(n*m).

The complexity of this operation comes from calling insert_te. The other operations in the function should run in O(1), with the key-loop having a max complexity of O(p) if it runs through every key in the list.

#### disable_te

disable_te has a complexity of O(m).

The key-loop has a maximal complexity of O(p), and changing the elements from 'A' to 'x' with a for-loop of length m runs in O(m). We will assume that m > p, because p depends on the order of the dictionary key list, and is therefore randomly sorted, while m is constant. The other operations in the function are simple, and are assumed to run in O(1) complexity.

#### active_te

active_te has a complexity of O(p)

Getting the key list from the dictionary, and returning the result both run in O(1) complexity. We assume that we have to run through the key dict_list to get it into a list, in which case it wil have O(p) complexity.

#### len

len runs in O(1), because evaluating the length of a list has O(1) complexity.

#### str

str runs in O(n)

str uses the join function, which has to run through each element in the genome to make it into a string. Therefore we expect the function ro run in O(n).

### Doubly-Linked-List Genome

#### init

init has a complexity of O(n).

Creating the genome by running through each element and appending takes n * O(1) = O(n) complexity. Creating hte ID and the TE-dictionary takes O(1).

#### insert_te

insert_te has a complecity of O(n)

We run through each element in the key-list (O(p)), checking if the new te either overlaps, or pushes the existing te's. This runs in max O(p). If there is a overlap, we run the disable_te function, that run in O(n). Creating the new TE takes O(m). Finding the start, where we want to insert our new TE takes a maximal O(n) complexity, if start is at the end of the genome. Inserting the new TE takes O(1). All of these run-times can then be reduced to O(n).

#### copy_te

copy_te has a complexity of O(n).

checking the keys has a maximum run-time of O(p), but our worst-case run-time must call the insert_te function. Therefore the run time of copy_te is defined by insert_te, which is defined by disable_te. Disable_te has a maximum complexity of O(n), and therefore, so does copy_te. 

#### disable_te

disable_te has a complexity of O(n).

Checking the key values takes a maximum of O(p) complexity. Only one key will fit our TE ID, so creating it within the loop only takes O(m) complexity. We create a **while i < start** loop, where i starts at 0, and has a maximum complexity of O(n), when the TE starts at the end of the genome. The **while j < length** loop runs in O(m) time. inserting the new disabled te should run in O(1), as should removing the now inactive key from the dictionary. The worst-time complexity for disable, is therefore proportional to the size of hte genome. 


#### active_te

active_te has a complexity of O(p)

We are still using a dictionary to present our active TE's, so the run time and reasoning is the same as before.

#### len

len has a complexity of O(n).

To get the length, we must loop through each element in the genome, creating a complecity of O(n).

#### str

str has a complexity of O(n^2)

Because we loop through the DLList, and use the += operation for the values, we end up with a complexity of O(n^2). This is not optimal, and might be optimised by first creating a list of the elements (O(n)), and then using the join function (O(1)).


In `src/simulate.py` you will find a program that can run simulations and tell you actual time it takes to simulate with different implementations. You can use it to test your analysis. You can modify the parameters to the simulator if you want to explore how they affect the running time.
