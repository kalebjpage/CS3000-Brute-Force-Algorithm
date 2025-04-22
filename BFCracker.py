import multiprocessing
import itertools
from hashlib import sha256
import functools

def CrackHashSingle(_passhash: str, _minlen: int, _maxlen: int, _charset: str) -> tuple[str|None, int]:
    guess_count = 0
    guessgen = GuessGenerator(_charset, _minlen, _maxlen)
    for guess in guessgen:
        guess_count += 1
        result = BFWorker(guess, _passhash)
        if result is not None:
            return (result, guess_count)
    return (None, guess_count)
    
def BFWorker(_guess: str, _tgthash: bytes):
    guesshash = sha256(_guess.encode()).digest()
    if guesshash == _tgthash:
        print("Found Password")
        return _guess
    return None

def GuessGenerator(_charset: str, _minlen: int, _maxlen: int):
    for passlen in range(_minlen, _maxlen+1):
        guess_product = itertools.product(_charset, repeat=passlen)
        for guess in guess_product:
            yield "".join(guess)

def CrackHashMulti(_passhash: bytes, _minlen: int, _maxlen: int, _charset: str) -> tuple[str | None, int]:
    guess_count = 0
    guess_gen = GuessGenerator(_charset, _minlen, _maxlen)
    process_num = multiprocessing.cpu_count()
    worker = functools.partial(BFWorker, _tgthash=_passhash)
    with multiprocessing.Pool(processes=process_num) as pool:
        for value in pool.imap_unordered(worker, guess_gen, chunksize=10000):
            guess_count += 1
            result = value
            if result is not None:
                return (result, guess_count)
    return (result, guess_count)

def GenerateCharset(_charcode: int):
    '''Takes in a 4 bit integer: 1 uses the subset, 0 doesn't use the subset'''
    low_charset = "abcdefghijklmnopqrstuvwxyz"
    upp_charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    num_charset = "0123456789"
    sym_charset = "~`!@#$%^&*()_-+={}[]|\\:;\"'<,>.?/"
    out_charset = ""
    if _charcode > 15 or _charcode < 0: # charcode out of bounds
        print("Invalid Charcode, must be 4 bits (<= 15, >= 0)")
        return out_charset
    if _charcode > 7:  # Bit #4
        out_charset += sym_charset
        _charcode -= 8
    if _charcode > 3:  # Bit #3
        out_charset += num_charset
        _charcode -= 4
    if _charcode > 1:  # Bit #2
        out_charset += upp_charset
        _charcode -= 2
    if _charcode > 0:  # Bit #1
        out_charset += low_charset
        _charcode -= 1
    return out_charset