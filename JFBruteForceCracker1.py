import multiprocessing
import itertools
from hashlib import sha256
import multiprocessing.managers

def CrackHash(_passhash: str, _minlen: int, _maxlen: int, _charset: str) -> tuple[str|None, int]:
    chars = _charset
    tgt_hash = _passhash
    guess_count = 0
    for cracklen in range(_minlen, _maxlen+1):
        print(f"Checking Passwords of length {cracklen}...")
        guess_generator = itertools.product(chars, repeat=cracklen)
        for guess_tup in guess_generator:
            guess = "".join(guess_tup)
            guess_hash = sha256(guess.encode())
            guess_count += 1
            if guess_hash == tgt_hash:
                return (guess, guess_count)
    return (None, guess_count)

def BFWorker(_guess: str, _tgthash: str):
    guesshash = sha256(_guess.encode()).digest()
    if guesshash == _tgthash:
        return _guess

def GuessGenerator(_charset: str, _minlen: int, _maxlen: int, _hash: str):
    for passlen in range(_minlen, _maxlen+1):
        guess_product = itertools.product(_charset, repeat=passlen)
        for guess in guess_product:
            yield ("".join(guess), _hash)

def CrackHashMulti(_passhash: str, _minlen: int, _maxlen: int, _charset: str, _processnum: int) -> tuple[str|None, int]:
    chars = _charset
    guess_gen = GuessGenerator(chars, _minlen, _maxlen, _passhash)
    guess_count = 0
    with multiprocessing.Pool(processes=_processnum) as pool:
        for result in pool.starmap_async(BFWorker, guess_gen).get():
            guess_count += 1
            print(guess_count)
            if result is not None:
                print("Result Found")
                return (result, guess_count)
    return (None, guess_count)

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

def main():
    password = "c"
    passhash = sha256(password.encode()).digest()
    print(f"Password: {password}")
    print(f"    Hash: {passhash}")
    print()
    guesses = -1
    crackedpassword, guesses = CrackHashMulti(passhash, 1, 3, GenerateCharset(1), 4)
    if crackedpassword is None:
        print(f"Password not found in {guesses} guesses")
    else:
        print(f"Password \"{crackedpassword}\" found in {guesses} guesses")

if __name__=="__main__":
    main()
