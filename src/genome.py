"""A circular genome for simulating transposable elements."""

from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)


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


class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        ...  # FIXME

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
        ...  # FIXME
        return -1

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
        ...  # FIXME

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # FIXME

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        # FIXME
        return []

    def __len__(self) -> int:
        """Current length of the genome."""
        # FIXME
        return 0

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
        return "FIXME"
