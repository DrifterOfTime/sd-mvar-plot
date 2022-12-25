from modules.hypernetworks import hypernetwork
import modules.sd_models as models
from modules.processing import StableDiffusionProcessingTxt2Img
import modules.shared as shared

from utils.modules.Module import Module

from utils.shortcodes import Shortcode as sc


class CFGScale(Module):
    """ Runs through multiple CFG scaling values.
    
    Methods are all inherited.
    """

    label = "CFGScale"
    field = "cfgscale"
    value_type = int

class CheckpointName(Module):
    """ Runs through multiple checkpoints
    """

    label = "Checkpoint Name"
    value_type = str

    def _confirm(cls):
        for x in cls.parsed_field_values:
            if models.get_closet_checkpoint_match(x) is None:
                raise RuntimeError(f"Unknown checkpoint: {x}")
    
    def apply(cls, p, loop_index):
        x = cls.parsed_field_values[loop_index]
        info = models.get_closet_checkpoint_match(x)
        if info is None:
            raise RuntimeError(f"Unknown checkpoint: {x}")
        models.reload_model_weights(shared.sd_model, info)
        p.sd_model = shared.sd_model

class CLIPSkip(Module):
    """ Runs through different levels of CLIP Skipping
    """

    label = "Clip Skip"
    value_type = int

    def apply(cls, p: StableDiffusionProcessingTxt2Img):
        x = cls.processedPrompt[cls.loopIndex]
        shared.opts.data["CLIP_stop_at_last_layers"] = x

class Denoising(Module):
    """
    Module
    """

    super().label = "Denoising"
    super().field = "denoising_strength"

class Hypernetwork(Module):
    """
    Module
    """

    super().label = "Hypernetwork"

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

    super().label = "Hypernet Strength"

    def apply(cls, p):
        x = cls.processedPrompt[cls.loopIndex]
        hypernetwork.apply_strength(x)

class ETA(Module):
    """
    Module
    """

    super().label = "ETA"
    super().field = "eta"

class MaskWeight(Module):
    """
    Module
    """

    super().label = "Mask Weight"
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

    super().label = "Permutation"

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

    super().label = "Prompt Matrix"

class PromptSR(Module):
    """
    Module
    """

    super().label = "Prompt S/R"

    def apply(cls, p, current_index):
        x = cls.processedPrompt[0]
        if x not in p.prompt and x not in p.negative_prompt:
            raise RuntimeError(f"Prompt S/R did not find {x} in prompt or negative prompt.")

        p.prompt = p.prompt.replace(x, )
        p.negative_prompt = p.negative_prompt.replace(x, )

    def format(cls):
        if type(value) == float:
            value = round(value, 8)
        return value

class Sampler(Module):
    """
    Module
    """

    super().label = "Sampler"

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
        if type(value) == float:
            value = round(value, 8)
        return value

class Seed(Module):
    """
    Module
    """

    super().label = "Seed"
    super().field = "seed"

class SigmaChurn(Module):
    """
    Module
    """

    super().label = "Sigma Churn"
    super().field = "s_churn"

class SigmaMax(Module):
    """
    Module
    """

    super().label = "Sigma Max"
    super().field = "s_tmax"

class SigmaMin(Module):
    """
    Module
    """

    super().label = "Sigma Min"
    super().field = "s_tmin"

class SigmaNoise(Module):
    """
    Module
    """

    super().label = "Sigma Noise"
    super().field = "s_noise"

class Step(Module):
    """
    Module
    """

    super().label = "Steps"
    super().field = "steps"

class VarSeed(Module):
    """
    Module
    """

    super().label = "Var. Seed"
    super().field = "subseed"

class VarStrength(Module):
    """
    Module
    """

    super().label = "Var. Strength"
    super().field = "subseed_strength"
    