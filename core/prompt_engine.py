class PromptEngineer:

    MAX_LENGTH = 2048

    @staticmethod
    def build_prompt(
        subject,
        composition="",
        style="",
        lighting="",
        colors="",
        required_elements=""
    ):

        sections = {
            "Subject": subject,
            "Composition": composition,
            "Visual style": style,
            "Lighting and atmosphere": lighting,
            "Color palette": colors,
            "Required elements": required_elements
        }

        if not subject or not subject.strip():
            raise ValueError(
                "O assunto principal da imagem é obrigatório."
            )

        prompt_parts = []

        for title, content in sections.items():

            if content and content.strip():

                clean_content = " ".join(
                    content.strip().split()
                )

                prompt_parts.append(
                    f"{title}: {clean_content}."
                )

        final_prompt = "\n".join(prompt_parts)

        if len(final_prompt) > PromptEngineer.MAX_LENGTH:
            raise ValueError(
                "O prompt estruturado ultrapassou "
                "o limite de 2048 caracteres."
            )

        return final_prompt
