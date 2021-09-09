from secrets import token_bytes

import pytest

import pyseto
from pyseto import DecryptError, EncryptError, Key


class TestV1Local:
    """
    Tests for v1.local.
    """

    @pytest.mark.parametrize(
        "key, msg",
        [
            (b"", "key must be specified."),
        ],
    )
    def test_v1_local_via_new_with_invalid_arg(self, key, msg):
        with pytest.raises(ValueError) as err:
            Key.new("v1", "local", key)
            pytest.fail("Key.new() should fail.")
        assert msg in str(err.value)

    def test_v1_local_via_decode_with_wrong_key(self):
        k1 = Key.new("v1", "local", b"our-secret")
        k2 = Key.new("v1", "local", b"others-secret")
        token = pyseto.encode(k1, b"Hello world!")
        with pytest.raises(DecryptError) as err:
            pyseto.decode(k2, token)
            pytest.fail("pyseto.decode() should fail.")
        assert "Failed to decrypt." in str(err.value)

    def test_v1_local_encrypt_with_invalid_arg(self):
        k = Key.new("v1", "local", b"our-secret")
        with pytest.raises(EncryptError) as err:
            k.encrypt(None)
            pytest.fail("pyseto.encrypt() should fail.")
        assert "Failed to encrypt." in str(err.value)

    @pytest.mark.parametrize(
        "nonce",
        [
            token_bytes(1),
            token_bytes(8),
            token_bytes(31),
            token_bytes(33),
            token_bytes(64),
        ],
    )
    def test_v1_local_via_encode_with_wrong_nonce(self, nonce):
        k = Key.new("v1", "local", b"our-secret")
        with pytest.raises(ValueError) as err:
            pyseto.encode(k, b"Hello world!", nonce=nonce)
            pytest.fail("pyseto.encode() should fail.")
        assert "nonce must be 32 bytes long." in str(err.value)
