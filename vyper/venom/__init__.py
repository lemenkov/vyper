# maybe rename this `main.py` or `venom.py`
# (can have an `__init__.py` which exposes the API).

from typing import Optional

from vyper.codegen.ir_node import IRnode
from vyper.compiler.settings import OptimizationLevel, Settings
from vyper.evm.address_space import MEMORY, STORAGE, TRANSIENT
from vyper.exceptions import CompilerPanic
from vyper.venom.analysis import MemSSA
from vyper.venom.analysis.analysis import IRAnalysesCache
from vyper.venom.context import IRContext
from vyper.venom.function import IRFunction
from vyper.venom.ir_node_to_venom import ir_node_to_venom
from vyper.venom.passes import (
    CSE,
    SCCP,
    AlgebraicOptimizationPass,
    AssignElimination,
    BranchOptimizationPass,
    CFGNormalization,
    DFTPass,
    FloatAllocas,
    FunctionInlinerPass,
    LoadElimination,
    LowerDloadPass,
    MakeSSA,
    Mem2Var,
    MemMergePass,
    PhiEliminationPass,
    ReduceLiteralsCodesize,
    RemoveUnusedVariablesPass,
    RevertToAssert,
    SimplifyCFGPass,
    SingleUseExpansion,
)
from vyper.venom.passes.dead_store_elimination import DeadStoreElimination
from vyper.venom.venom_to_assembly import VenomCompiler

DEFAULT_OPT_LEVEL = OptimizationLevel.default()


def generate_assembly_experimental(
    runtime_code: IRContext,
    deploy_code: Optional[IRContext] = None,
    optimize: OptimizationLevel = DEFAULT_OPT_LEVEL,
) -> list[str]:
    # note: VenomCompiler is sensitive to the order of these!
    if deploy_code is not None:
        functions = [deploy_code, runtime_code]
    else:
        functions = [runtime_code]

    compiler = VenomCompiler(functions)
    return compiler.generate_evm(optimize == OptimizationLevel.NONE)


def _run_passes(fn: IRFunction, optimize: OptimizationLevel, ac: IRAnalysesCache) -> None:
    # Run passes on Venom IR
    # TODO: Add support for optimization levels

    FloatAllocas(ac, fn).run_pass()

    SimplifyCFGPass(ac, fn).run_pass()

    MakeSSA(ac, fn).run_pass()
    PhiEliminationPass(ac, fn).run_pass()

    # run constant folding before mem2var to reduce some pointer arithmetic
    AlgebraicOptimizationPass(ac, fn).run_pass()
    SCCP(ac, fn, remove_allocas=False).run_pass()
    SimplifyCFGPass(ac, fn).run_pass()

    AssignElimination(ac, fn).run_pass()
    Mem2Var(ac, fn).run_pass()
    MakeSSA(ac, fn).run_pass()
    PhiEliminationPass(ac, fn).run_pass()
    SCCP(ac, fn).run_pass()

    SimplifyCFGPass(ac, fn).run_pass()
    AssignElimination(ac, fn).run_pass()
    AlgebraicOptimizationPass(ac, fn).run_pass()

    LoadElimination(ac, fn).run_pass()

    SCCP(ac, fn).run_pass()
    AssignElimination(ac, fn).run_pass()
    RevertToAssert(ac, fn).run_pass()

    SimplifyCFGPass(ac, fn).run_pass()
    MemMergePass(ac, fn).run_pass()
    RemoveUnusedVariablesPass(ac, fn).run_pass()

    DeadStoreElimination(ac, fn).run_pass(addr_space=MEMORY)
    DeadStoreElimination(ac, fn).run_pass(addr_space=STORAGE)
    DeadStoreElimination(ac, fn).run_pass(addr_space=TRANSIENT)
    LowerDloadPass(ac, fn).run_pass()

    BranchOptimizationPass(ac, fn).run_pass()

    AlgebraicOptimizationPass(ac, fn).run_pass()

    # This improves the performance of cse
    RemoveUnusedVariablesPass(ac, fn).run_pass()

    PhiEliminationPass(ac, fn).run_pass()
    AssignElimination(ac, fn).run_pass()
    CSE(ac, fn).run_pass()

    AssignElimination(ac, fn).run_pass()
    RemoveUnusedVariablesPass(ac, fn).run_pass()
    SingleUseExpansion(ac, fn).run_pass()

    if optimize == OptimizationLevel.CODESIZE:
        ReduceLiteralsCodesize(ac, fn).run_pass()

    DFTPass(ac, fn).run_pass()

    CFGNormalization(ac, fn).run_pass()


def _run_global_passes(ctx: IRContext, optimize: OptimizationLevel, ir_analyses: dict) -> None:
    FunctionInlinerPass(ir_analyses, ctx, optimize).run_pass()


def run_passes_on(ctx: IRContext, optimize: OptimizationLevel) -> None:
    ir_analyses = {}
    for fn in ctx.functions.values():
        ir_analyses[fn] = IRAnalysesCache(fn)

    _run_global_passes(ctx, optimize, ir_analyses)

    ir_analyses = {}
    for fn in ctx.functions.values():
        ir_analyses[fn] = IRAnalysesCache(fn)

    for fn in ctx.functions.values():
        _run_passes(fn, optimize, ir_analyses[fn])


def generate_ir(ir: IRnode, settings: Settings) -> IRContext:
    # Convert "old" IR to "new" IR
    ctx = ir_node_to_venom(ir)

    optimize = settings.optimize
    assert optimize is not None  # help mypy
    run_passes_on(ctx, optimize)

    return ctx
