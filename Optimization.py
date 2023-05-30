import llvmlite.binding as llvm


class Optimization:
    def __init__(self,module_ref):
        self.module_ref = module_ref
        pass_manager_builder = llvm.create_pass_manager_builder()

        module_pass_manager = llvm.create_module_pass_manager()

        module_pass_manager.add_constant_merge_pass()
        module_pass_manager.add_dead_arg_elimination_pass()
        module_pass_manager.add_function_attrs_pass()
        module_pass_manager.add_function_inlining_pass(5)
        module_pass_manager.add_global_dce_pass()
        module_pass_manager.add_global_optimizer_pass()
        module_pass_manager.add_ipsccp_pass()
        module_pass_manager.add_dead_code_elimination_pass()
        module_pass_manager.add_cfg_simplification_pass()
        module_pass_manager.add_gvn_pass()
        module_pass_manager.add_instruction_combining_pass()
        module_pass_manager.add_licm_pass()
        module_pass_manager.add_sccp_pass()
        module_pass_manager.add_sroa_pass()
        module_pass_manager.add_type_based_alias_analysis_pass()
        module_pass_manager.add_basic_alias_analysis_pass()

        pass_manager_builder.populate(module_pass_manager)

        module_pass_manager.run(module_ref)