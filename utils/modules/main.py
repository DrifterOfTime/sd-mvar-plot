from utils.modules.MVModuleBase import MVModuleBase

class CFGScale(MVModuleBase):
    """
    Module
    """

    super().setLabel("CFGScale")
    super().setField("cfgscale")

class CheckpointName(MVModuleBase):
    """
    Module
    """

    super().setLabel("Checkpoint Name")

    def confirm(cls):
        for x in cls.processedPrompt:
            if models.get_closet_checkpoint_match(x) is None:
                raise RuntimeError(f"Unknown checkpoint: {x}")
    
    def apply(cls, p):
        x = cls.processedPrompt[cls.loopIndex]
        info = models.get_closet_checkpoint_match(x)
        if info is None:
            raise RuntimeError(f"Unknown checkpoint: {x}")
        models.reload_model_weights(shared.sd_model, info)
        cls.p.sd_model = shared.sd_model

class ClipSkip(MVModuleBase):
    """
    Module
    """

    super().setLabel("Clip Skip")

    def apply(cls, p: StableDiffusionProcessingTxt2Img):
        x = cls.processedPrompt[cls.loopIndex]
        shared.opts.data["CLIP_stop_at_last_layers"] = x

class Denoising(MVModuleBase):
    """
    Module
    """

    super().setLabel("Denoising")
    super().setField("denoising_strength")

class Hypernetwork(MVModuleBase):
    """
    Module
    """

    super().setLabel("Hypernetwork")

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

class HypernetworkStrength(MVModuleBase):
    """
    Module
    """

    super().setLabel("Hypernet Strength")

    def apply(cls, p):
        x = cls.processedPrompt[cls.loopIndex]
        hypernetwork.apply_strength(x)

class ETA(MVModuleBase):
    """
    Module
    """

    super().setLabel("ETA")
    super().setField("eta")

class MaskWeight(MVModuleBase):
    """
    Module
    """

    super().setLabel("Mask Weight")
    super().setField("inpainting_mask_weight")

class Permutation(MVModuleBase):
    """
    Module
    """
    super().setLabel("Permutation")

    def apply(cls):
        
        token_order = []

        # Initally grab the tokens from the prompt, so they can be replaced in order of earliest seen
        for token in cls.processedPrompt:
            token_order.append((p.prompt.find(token), token))

        token_order.sort(key=lambda t: t[0])

        prompt_parts = []

        # Split the prompt up, taking out the tokens
        for _, token in token_order:
            n = p.prompt.find(token)
            prompt_parts.append(p.prompt[0:n])
            p.prompt = p.prompt[n + len(token):]

        # Rebuild the prompt with the tokens in the order we want
        prompt_tmp = ""
        for idx, part in enumerate(prompt_parts):
            prompt_tmp += part
            prompt_tmp += cls.processedPrompt[idx]
        p.prompt = prompt_tmp + p.prompt

    def format(cls): return ", ".join(cls.processedPrompt)

class PromptMatrix(MVModuleBase):
    """
    Module
    """

    super().setLabel("Prompt Matrix")

class PromptSR(MVModuleBase):
    """
    Module
    """

    super().setLabel("Prompt S/R")

    def apply(cls):
        x = cls.processedPrompt[0]
        if x not in p.prompt and x not in p.negative_prompt:
            raise RuntimeError(f"Prompt S/R did not find {x} in prompt or negative prompt.")

        p.prompt = p.prompt.replace(x, )
        p.negative_prompt = p.negative_prompt.replace(x, )

    def format(cls):
        if type(value) == float:
            value = round(value, 8)
        return value

class Sampler(MVModuleBase):
    """
    Module
    """

    super().setLabel("Sampler")

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

class Seed(MVModuleBase):
    """
    Module
    """

    super().setLabel("Seed")
    super().setField("seed")

class SigmaChurn(MVModuleBase):
    """
    Module
    """

    super().setLabel("Sigma Churn")
    super().setField("s_churn")

class SigmaMax(MVModuleBase):
    """
    Module
    """

    super().setLabel("Sigma Max")
    super().setField("s_tmax")

class SigmaMin(MVModuleBase):
    """
    Module
    """

    super().setLabel("Sigma Min")
    super().setField("s_tmin")

class SigmaNoise(MVModuleBase):
    """
    Module
    """

    super().setLabel("Sigma Noise")
    super().setField("s_noise")

class Step(MVModuleBase):
    """
    Module
    """

    super().setLabel("Steps")
    super().setField("steps")

class VarSeed(MVModuleBase):
    """
    Module
    """

    super().setLabel("Var. Seed")
    super().setField("subseed")

class VarStrength(MVModuleBase):
    """
    Module
    """

    super().setLabel("Var. Strength")
    super().setField("subseed_strength")
    