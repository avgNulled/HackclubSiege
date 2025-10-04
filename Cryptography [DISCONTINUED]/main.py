# Imports Modules
import os, sys
import socket

import csv, json

from datetime import datetime

import numpy as np
import pandas as pd

from hashlib import sha256

from typing import List, Tuple, Dict, Union, Optional, Any


# Defines Block Class
class Block:
    """Python Blockchain Single-Block Class"""
    def __init__(self, index: int, timestamp: datetime, data: str, previous_hash: str = "") -> None:
        # Block Variables
        self.index, self.timestamp, self.data, self.previous_hash = index, timestamp, data, previous_hash
        self.hash = ""

    def _block_hash_init(self) -> str:
        """Init Block Hash"""
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}".encode()
        return sha256(block_string).hexdigest()
    

# Defines Blockchain Class
class Blockchain:
    """Python Blockchain Class"""
    def __init__(self) -> None:
        # Defines Blocks
        self.blocks: List[Block] = []
        self.valid = True

        # Init Geneis Block
        self._init_geneis_block()
    
    def write_to_json(self, path: str, /, force: bool = False) -> None:
        """Writes Blockchain to Path"""
        if not os.path.exists(path) or force:
            with open(path, "w") as f:
                json.dump({block.index: block.hash for block in self.blocks}, f, indent=2)
        
        return
    
    def write_to_csv(self, path: str, /, force: bool = False) -> None:
        """Writes Blockchain to Path"""
        if not os.path.exists(path) or force:
            with open("path", "w") as f:
                csv_writer = csv.writer(f)

                csv_writer.writerows("")
    
    def add_block(self, new_block: Block) -> None:
        """Adds Block to Blockchain"""
        new_block.previous_hash = self.get_last_block().hash
        new_block._block_hash_init()

        self.blocks.append(new_block)
    
    def verify(self) -> bool:
        """Verifies Blockchain"""
        valid = True

        for i in range(1, len(self.blocks)):
            # Verifies Hash According to Previous Hash
            if self.blocks[i].previous_hash != self.blocks[i-1].hash:
                valid = False
                break
            
            # Verifies Hash According to Hash Function
            if self.blocks[i].hash != self.blocks[i-1]._block_hash_init():
                valid = False
                break
        
        
        self.valid = valid
        return self.valid
    
    def _verify(self) -> None:
        """Verifies Blockchain Integrity"""

        for i in range(1, len(self.blocks)):
            # Verifies Hash According to Previous Hash
            if self.blocks[i].previous_hash != self.blocks[i-1].hash:
                self.valid = False
                break
            
            # Verifies Hash According to Hash Function
            if self.blocks[i].hash != self.blocks[i-1]._block_hash_init():
                self.valid = False
                break
        
        return
        
    def get_last_block(self) -> Block:
        """Returns Last Added Block"""
        return self.blocks[-1]

    def pop_last_block(self) -> Block:
        """Pops Last Blocks"""
        return self.blocks.pop(-1)
    
    def _init_geneis_block(self) -> None:
        """Init Geneis Block"""
        geneis_block = Block(0, datetime.now(), "")
        geneis_block.hash = geneis_block._block_hash_init()

        self.blocks.append(geneis_block)


# Defines Wallet
class Wallet:
    """Blockchain Wallet Class"""
    def __init__(self) -> None:
        self.balance = 0.0
        
    def _add_balance(self, amount: float) -> None:
        self.balance += amount