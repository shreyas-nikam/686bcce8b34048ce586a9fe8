
import re
from typing import TypeVar, Any

# In a production environment, 'Symbol' would typically be imported from an external library
# (e.g., `from symai import Symbol`). For this isolated code stub, we define a minimal
# placeholder class that provides the expected interface (a 'value' attribute) to satisfy
# the type hint's bound constraint and allow the code to run in a test environment
# where the actual 'symai.Symbol' might not be available.
class Symbol:
    """
    A placeholder base class for Symbol objects, used primarily for type hinting.
    In a real application, this would represent the `symai.Symbol` class.
    It expects to hold a value that can be converted to a string.
    """
    def __init__(self, value: Any):
        self._value = value

    @property
    def value(self) -> Any:
        """The underlying value of the Symbol, typically text content."""
        return self._value

    # These dunder methods are included for completeness and consistent behavior
    # with Symbol-like objects, although not strictly required by clean_symbol's logic.
    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self._value!r})"


# Define a type variable for generic Symbol-like objects.
# This allows type checkers to ensure that the input and output types are consistent.
# The `bound=Symbol` ensures that any type used for SymbolLike must be a subclass of our
# placeholder Symbol (or the actual symai.Symbol in production).
SymbolLike = TypeVar('SymbolLike', bound=Symbol)

def clean_symbol(input_symbol: SymbolLike) -> SymbolLike:
    """
    Simulates text cleaning, such such as removing special characters or extra spaces,
    from a Symbol object. This operation transforms the input text into a cleaner
    format, resulting in a new Symbol instance.

    The cleaning process applies the following steps to the Symbol's internal text value:
    1.  Strips any leading and trailing whitespace characters.
    2.  Replaces sequences of multiple whitespace characters (including spaces, newlines,
        tabs, etc.) with a single space.
    3.  Removes any characters that are not alphanumeric (letters, numbers, underscore)
        or a single space. Punctuation and other symbols are removed.

    Arguments:
        input_symbol (SymbolLike): The Symbol object containing the text to be cleaned.
                                   This object must expose its text content via a 'value'
                                   attribute.

    Returns:
        SymbolLike: A new Symbol object of the same concrete type as the input_symbol,
                    containing the cleaned text. The returned object is a distinct instance
                    from the input_symbol, ensuring the original object remains unchanged.

    Raises:
        TypeError: If `input_symbol` is not a Symbol-like object (i.e., it does not
                   have a 'value' attribute). This handles cases like `None`, plain
                   strings, numbers, lists, or dictionaries passed directly instead of
                   being wrapped in a Symbol object.
    """
    # Error handling: Ensure the input is a Symbol-like object with a 'value' attribute.
    if not hasattr(input_symbol, 'value'):
        raise TypeError(
            f"Input must be a Symbol-like object with a 'value' attribute, "
            f"but received an object of type {type(input_symbol).__name__}."
        )

    # Extract the raw text value from the Symbol object.
    # We explicitly convert it to a string to handle cases where the Symbol's
    # value might be an integer, list, dictionary, or other non-string type
    # that needs to be represented as text for cleaning.
    original_text = str(input_symbol.value)

    # Step 1: Remove leading and trailing whitespace.
    text_stripped = original_text.strip()

    # Step 2: Normalize internal whitespace. Replace any sequence of one or more
    # whitespace characters (spaces, tabs, newlines) with a single space.
    text_normalized_spaces = re.sub(r'\s+', ' ', text_stripped)

    # Step 3: Remove non-alphanumeric and non-space characters.
    # `\w` matches alphanumeric characters (letters, numbers, and underscore).
    # `\s` matches any whitespace character (which is now guaranteed to be single spaces).
    # `[^\w\s]` matches anything that is NOT a word character and NOT a whitespace character.
    cleaned_text = re.sub(r'[^\w\s]', '', text_normalized_spaces)

    # Return a new Symbol object initialized with the cleaned text.
    # `input_symbol.__class__` ensures that the new object is of the same
    # specific class (e.g., MockSymbol) as the input, preserving type.
    return input_symbol.__class__(cleaned_text)
