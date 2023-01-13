import modules.sd_models as models
import modules.shared as shared
from modules import sd_models, sd_samplers, shared
from modules.hypernetworks import hypernetwork
from modules.processing import StableDiffusionProcessingTxt2Img
from modules.shared import opts

from utils.modules.__IModuleTypes import *


class Nothing(IModuleOther):
    def __init__(cls, raw_values):
        cls.name = "Nothing"

class CFGScale(IModuleInt):
    """ Runs through multiple CFG scaling values.
    
    Methods are all inherited.
    """
    def __init__(cls, raw_values):
        super().__init__(raw_values)
        cls.name = "CFGScale"
        cls._field = "cfgscale"

class CheckpointName(IModuleStr):
    """ Runs through multiple checkpoints
    """
    def __init__(cls, raw_values):
        super().__init__(raw_values)
        cls.name = "Checkpoint Name"

    def __enter__(cls):
        cls._original_value = shared.sd_model

    def __exit__(cls, exc_type, exc_value, tb):
        sd_models.reload_model_weights(cls._original_value)

    def __check(cls):
        value = cls._get_value()
        if models.get_closet_checkpoint_match(value) is None:
            print(f"Unknown checkpoint: {value}")
            return False
        else: return True
    
    def __apply(cls, p):
        value = cls._get_value()
        if cls._confirm():
            info = models.get_closet_checkpoint_match(value)
            models.reload_model_weights(shared.sd_model, info)
            p.sd_model = shared.sd_model
            return True
        return False

class CLIPSkip(IModuleInt):
    """ Runs through different levels of CLIP Skipping
    """

    label = "Clip Skip"
    _option = "CLIP_stop_at_last_layers"

    def __enter__(cls):
        cls._original_value = opts.data[cls._option]

    def __exit__(cls, exc_type, exc_value, tb):
        opts.data[cls._option] = cls._original_value

    def __apply(cls, p: StableDiffusionProcessingTxt2Img):
        cls._check()
        x = cls._values[cls._current_index]
        shared.opts.data["CLIP_stop_at_last_layers"] = x

class Denoising(Module):
    """
    Module
    """

    name = "Denoising"
    _field = "denoising_strength"

class Hypernetwork(Module):
    """
    Module
    """

    super().name = "Hypernetwork"

    def confirm(cls, p):
        for x in cls.processedPrompt:
            if x.lower() in ["", "none"]:
                continue
            if not hypernetwork.find_closest_hypernetwork_name(x):
                raise RuntimeError(f"Unknown hypernetwork: {x}")

    def apply(cls, p):
        x = cls.processedPrompt[cls.loopIndex]
        if x.lower() in ["", "none"]:
            name = None
        else:
            name = hypernetwork.find_closest_hypernetwork_name(x)
            if not name:
                raise RuntimeError(f"Unknown hypernetwork: {x}")
        hypernetwork.load_hypernetwork(name)

class HypernetworkStrength(Module):
    """
    Module
    """

    super().name = "Hypernet Strength"

    def apply(cls, p):
        x = cls.processedPrompt[cls.loopIndex]
        hypernetwork.apply_strength(x)

class ETA(Module):
    """
    Module
    """

    super().name = "ETA"
    super().field = "eta"

class MaskWeight(Module):
    """
    Module
    """

    super().name = "Mask Weight"
    super().field = "inpainting_mask_weight"

class Permutation(Module):
    """ Takes certain values in the prompt and runs through every permutation of them

    Public Attributes:
        label: (`str`):
            Inherited from `_Module`
        field: (`str`):
            Inherited from `_Module`. No field for permutations in `p`, so empty string

    Public Methods:
        apply(p, field_values, current_index)
        format(p, options, field_values, current_index)
    """

    super().name = "Permutation"

    def apply(cls, p: StableDiffusionProcessingTxt2Img, field_values, current_index):
        """ Permutes `field_values` in `p.prompt`

        Args:
            p (`StableDiffusionProcessingTxt2Img`)
            field_values (`list(Any)`):
                Values to be permuted
            current_index (`int`):
                Dummy value in this function (function permutes prompt in `p` itself)
        """
        
        token_order = []

        # Initally grab the tokens from the prompt, so they can be replaced in order of earliest seen
        for token in field_values:
            token_location = p.prompt.find(token)
            if token_location > -1: 
                token_order.append((token_location, token))
            else:
                raise ValueError(f"Permutation Module: \"{token}\" not found in prompt")

        token_order.sort(key=lambda t: t[0])

        prompt_parts = []

        # Split the prompt up, taking out the tokens
        for _, token in token_order:
            prompt_parts.append(p.prompt[0:token_location])
            p.prompt = p.prompt[token_location + len(token):]

        # Rebuild the prompt with the tokens in the order we want
        token_permutation = ""
        for idx, part in enumerate(prompt_parts):
            token_permutation += part
            token_permutation += field_values[idx]
        p.prompt = token_permutation + p.prompt

    def format(cls, p, options, field_values, current_index): return ", ".join(field_values)

class PromptMatrix(Module):
    """
    Module
    """

    super().name = "Prompt Matrix"

class PromptSR(Module):
    """
    Module
    """

    super().name = "Prompt S/R"

    def apply(cls, p, current_index):
        x = cls.processedPrompt[0]
        if x not in p.prompt and x not in p.negative_prompt:
            raise RuntimeError(f"Prompt S/R did not find {x} in prompt or negative prompt.")

        p.prompt = p.prompt.replace(x, )
        p.negative_prompt = p.negative_prompt.replace(x, )

    def format(cls):
        if types(value) == float:
            value = round(value, 8)
        return value

class Sampler(Module):
    """
    Module
    """

    super().name = "Sampler"

    def confirm(cls):
        for x in cls.processedPrompt:
            if x.lower() not in samplers.samplers_map:
                raise RuntimeError(f"Unknown sampler: {x}")

    def apply(cls):
        for x in cls.processedPrompt:
            sampler_name = samplers.samplers_map.get(x.lower(), None)
            if sampler_name is None:
                raise RuntimeError(f"Unknown sampler: {x}")

            p.sampler_name = sampler_name
    
    def format(cls):
        if types(value) == float:
            value = round(value, 8)
        return value

class Seed(Module):
    """
    Module
    """

    super().name = "Seed"
    super().field = "seed"

class SigmaChurn(Module):
    """
    Module
    """

    super().name = "Sigma Churn"
    super().field = "s_churn"

class SigmaMax(Module):
    """
    Module
    """

    super().name = "Sigma Max"
    super().field = "s_tmax"

class SigmaMin(Module):
    """
    Module
    """

    super().name = "Sigma Min"
    super().field = "s_tmin"

class SigmaNoise(Module):
    """
    Module
    """

    super().name = "Sigma Noise"
    super().field = "s_noise"

class Step(Module):
    """
    Module
    """

    super().name = "Steps"
    super().field = "steps"

class VarSeed(Module):
    """
    Module
    """

    super().name = "Var. Seed"
    super().field = "subseed"

class VarStrength(Module):
    """
    Module
    """

    super().name = "Var. Strength"
    super().field = "subseed_strength"
    