import ctypes
import os
import sys

import llvmlite.binding as llvm
from CodeGenerator import Block, GenerateCode, prTr
from Optimization import Optimization
from Parser import build_tree, getTable


def run(llvm_ir):
    mod = llvm.parse_assembly(str(llvm_ir.module))
    mod.verify()


    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine(codemodel="small")

    llvm_ir.module.triple = llvm.get_default_triple()
    llvm_ir.module.data_layout = target_machine.target_data


    print("\nCODE WITH OPTIMIZATION:")
    Optimization(mod)
    print(mod)

    print('\nASSEMBLER OUTPUT:')
    asm = target_machine.emit_assembly(mod)
    open('Code.asm', 'w').write(str(asm))
    print(asm)

    obj = target_machine.emit_object(mod)
    open('Code.o', 'wb').write(obj)

    print('\nOUTPUT:')
    os.system(f"clang Code.o -o Code.exe")
    os.system("Code.exe")


def main():
    from llvmGenerator import compile_llvm

    source = open("C:/Users/Denis/PycharmProjects/Compiler1/Codes/Code.txt").read()

    tree = build_tree(source)

    if tree:
        print("\nPARSING TREE:")
        print(tree)

        print("\nTABLE OF SYMBOLS:")
        print(getTable(tree))

        bloc = Block()
        bloc.inithead('Main')
        bloc = GenerateCode(bloc, tree, 'global', False, getTable(tree))

        print("\nTREE-ADDRESS CODE:")
        prTr(bloc, 1)
        generator = compile_llvm(bloc)
        llvm_code = str(generator.module)

        print("\nLLVM CODE:")
        print(llvm_code)

        run(generator)



if __name__ == '__main__':
    main()
