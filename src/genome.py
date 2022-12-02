"""A circular genome for simulating transposable elements."""

from __future__ import annotations
from typing import (
    Generic, TypeVar, Iterable,
    Callable, Protocol
)

from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)

#### The linked list and doubly linked list class from the doubly-linked-lists exercises (copied directly over)

class Comparable(Protocol):
    """Type info for specifying that objects can be compared with <."""

    def __lt__(self, other: Comparable) -> bool:
        """Less than, <, operator."""
        ...


T = TypeVar('T')
S = TypeVar('S', bound=Comparable)


class Link(Generic[T]):
    """Doubly linked link."""

    val: T
    prev: Link[T]
    next: Link[T]

    def __init__(self, val: T, p: Link[T], n: Link[T]):
        """Create a new link and link up prev and next."""
        self.val = val
        self.prev = p
        self.next = n


def insert_after(link: Link[T], val: T) -> None:
    """Add a new link containing val after link."""
    new_link = Link(val, link, link.next)
    new_link.prev.next = new_link
    new_link.next.prev = new_link


def remove_link(link: Link[T]) -> None:
    """Remove link from the list."""
    link.prev.next = link.next
    link.next.prev = link.prev


class DLList(Generic[T]):
    """
    Wrapper around a doubly-linked list.

    This is a circular doubly-linked list where we have a
    dummy link that function as both the beginning and end
    of the list. By having it, we remove multiple special
    cases when we manipulate the list.

    >>> x = DLList([1, 2, 3, 4])
    >>> print(x)
    [1, 2, 3, 4]
    """

    head: Link[T]  # Dummy head link

    def __init__(self, seq: Iterable[T] = ()):
        """Create a new circular list from a sequence."""
        # Configure the head link.
        # We are violating the type invariants this one place,
        # but only here, so we ask the checker to just ignore it.
        # Once the head element is configured we promise not to do
        # it again.
        self.head = Link(None, None, None)  # type: ignore
        self.head.prev = self.head
        self.head.next = self.head

        # Add elements to the list, exploiting that self.head.prev
        # is the last element in the list, so appending means inserting
        # after that link.
        for val in seq:
            insert_after(self.head.prev, val)

    def __str__(self) -> str:
        """Get string with the elements going in the next direction."""
        elms: list[str] = []
        link = self.head.next
        while link and link is not self.head:
            elms.append(str(link.val))
            link = link.next
        return f"[{', '.join(elms)}]"
    __repr__ = __str__  # because why not?

#### The abstract genome class

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

#### The list genome class

class ListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using Python's built-in lists
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.genome = ['-'] * n # the new genome has no tes, so it is represented as - for the entire length
        self.te = dict() # create a dictionary for te's, with ID's as keys and [pos, length] within them
        self.id = 0 # ID start for the te's

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
        self.id += 1 # Create new id for new te element
        self.te[self.id] = [pos, length] # create new element in te dictionary, with ID as the key, and position and length in list
        key_list = list(self.te.keys()) # get all keys in te dictionary
        for key in key_list: # itterate over each element in the te dictionary
            start = self.te[key][0] # start-position of te
            end = start + self.te[key][1] # end position of the te
            if start < pos <= end: # if the position is in within this range, the new te inserts into the old one, and we must deactivate the old one
                for i in range(start, end): # used to change old te to an inactive te, we use a for-loop so we don't change start, which we need in line 124
                    self.genome[i] = 'x' # changing 'A' to 'x' for old te
                del self.te[key] # remove old te, as it is now inactive
            if pos < start: # updating the start position, and also key for all te after position of new te. We need it to be start<pos, because if we also had start=pos, we would always move the pos of the new element
                new_start = start + length # old te is pushed the equivalent of the length of the new te
                self.te[key][0] = new_start # update start position for the old te
        te = ['A'] * length # create new te
        self.genome[pos:pos] = te # insert new te
        return self.id # this should be the ID for the new te

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
        if te in self.te.keys(): # checks if te-ID is in the te dictionary
            l = self.te[te][1] # length of original te will be the same as the one that is being copied
            p = (self.te[te][0] + offset) % len(self) # This should do math magic to make it fit inside the genome interval
            self.insert_te(p, l) # we ise the insert_te function, that is defined above
            return self.id
        else:
            return None

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        if te in self.te.keys(): # checks if te-ID is in the te dictionary
            start = self.te[te][0] # start-position of te
            end = start + self.te[te][1] # end position of te
            for i in range(start, end): # itterate over te
                self.genome[i] = 'x' # changing 'A' to 'x' for old te
            del self.te[te]
        return None
            
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return list(self.te.keys()) # this function returns a list of all the keys in the dictionary, and we use te ID as keys, soooo...

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.genome) # Because we are implementing the class as a list, we can simply use the len function for the genome

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
        return ''.join(self.genome) # Because we are implementing the class as a list, we can use the join function to take each element in the genome, and put them together as a complete string

#### The linked list genome class

class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.genome = DLList(['-']*n) # we create the genome as a doubly linked list, using the already existing DLList __init__
        self.te = dict() # I use the same dictionary format for TE's as I did with the list implementation
        self.id = 0 # ID start for the te's

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
        self.id += 1 # Create new id for new te element
        self.te[self.id] = [pos, length] # create new element in te dictionary, with ID as the key, and position and length in list
        key_list = list(self.te.keys()) # get all keys in te dictionary
        for key in key_list: # itterate over each element in the te dictionary
            start = self.te[key][0] # start-position of te
            end = start + self.te[key][1] # end position of the te
            if start < pos <= end: # if the position is in within this range, the new te inserts into the old one, and we must deactivate the old one
                self.disable_te(key)
            if pos < start: # updating the start position, and also key for all te after position of new te. We need it to be start<pos, because if we also had start=pos, we would always move the pos of the new element
                new_start = start + length # old te is pushed the equivalent of the length of the new te
                self.te[key][0] = new_start # update start position for the old te
        te = DLList(['A'] * length) # create new te
        link_s = self.genome.head # we define the first element of the genome
        i = 0 # we have i as our index for the first while loop
        while i < start: # while i is smaller than the start...
            link_s = link_s.next # ... we move through the genome, to get to the start position of our new te
            i += 1
        link_e = link_s.next # the link of the genome after our start
        # We want to inser out new te between link_s and link_e
        link_s.next = te.head.next
        te.head.next.prev = link_s
        link_e.prev = te.head.prev
        te.head.prev.next = link_e
        return self.id # this should be the ID for the new te

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
        if te in self.te.keys(): # checks if te-ID is in the te dictionary
            start = self.te[te][0] # start-position of the original te
            length = self.te[te][1] # length of the original and new te
            offset = offset % len(self) # we modulus the offset by the length of the genome, because math magic makes it get the right position, even after looping or being negative
            te_start = start + offset
            self.insert_te(te_start, length)
            return self.id
        return None
    
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        # I could probably use the remove functions, but they only remove one value at a time. I think this uses the class's properties better
        if te in self.te.keys(): # checks if te-ID is in the te dictionary
            start = self.te[te][0] # start-position of te
            length = self.te[te][1] # length of te
            disabled_te = DLList(['x']*length) # we create a doubly-linked list representing the disabled te
            link_s = self.genome.head # we define the head element of the genome
            i = 0 # we have i as our index for the first while loop
            while i < start: # while i is smaller than the start...
                link_s = link_s.next # ... we move through the genome, to get to the start position of our te
                i += 1
            link_e = link_s # we want another link, representing the end of the te
            j = 0 # we have j as our index for the second while loop
            while j <= length: # as long as j is smaller than or equal to length...
                link_e = link_e.next # ... we move along the genome, to find the link next to our te
                j += 1
            # the next four lines link the disabled te to the genome, thereby removing the active genome
            link_s.next = disabled_te.head.next
            disabled_te.head.prev.next = link_e
            link_e.prev = disabled_te.head.prev
            disabled_te.head.next.prev = link_s
            del self.te[te] # we remove the disabled genome from the dictionary of active te's
        return None

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return list(self.te.keys()) # As before, with the string implementation, we can get a list of the active te-IDs from the keys in out te dictionary

    def __len__(self) -> int:
        """Current length of the genome."""
        length = 0 # we start with defining length as 0
        link = self.genome.head.next # this should be the first link in our genome. If the genome is empty, self.genome.head.next is the same as self.genome.head
        while link and link is not self.genome.head: # we itterate over each link in the genome, untill we loop back to the dummy-head of the doubly-linked list
            length += 1 # For each element in the genome that is not the head, the length grows by one
            link = link.next # we need to remember to update the link, so as not to create an infinite loop
        return length # we return the length, and if the genome is empty, it should be 0

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
        elms: str = ''
        link = self.genome.head.next
        while link and link is not self.genome.head:
            elms += (str(link.val))
            link = link.next
        return elms # This is a slight modification of the dunder str function for the DLList class
