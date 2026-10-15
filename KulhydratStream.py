import math
import re
import streamlit as st


# --- DIN KEMISKE LOGIK (UÆNDRET) ---
def afstem_forbraending(formel: str) -> str:
    formel = formel.strip()
    if not re.fullmatch(r"(?:[A-Z][a-z]?\d*)+", formel):
        raise ValueError(
            "Formlen skal bestå af grundstofsymboler og tal, fx C6H12O6."
        )

    atomer = {"C": 0, "H": 0, "O": 0}
    for grundstof, antal in re.findall(r"([A-Z][a-z]?)(\d*)", formel):
        if grundstof not in atomer:
            raise ValueError("Kun grundstofferne C, H og O understøttes.")
        atomer[grundstof] += int(antal) if antal else 1

    if any(antal == 0 for antal in atomer.values()):
        raise ValueError("Formlen skal indeholde C, H og O.")

    kulstof = atomer["C"]
    hydrogen = atomer["H"]
    oxygen = atomer["O"]
    oxygenkoefficient = 4 * kulstof + hydrogen - 2 * oxygen

    koefficienter = [4, abs(oxygenkoefficient), 4 * kulstof, 2 * hydrogen]
    divisor = math.gcd(*koefficienter)
    koefficienter = [koefficient // divisor for koefficient in koefficienter]

    forbindelse, ilt, kuldioxid, vand = koefficienter

    def led(koefficient: int, stof: str) -> str:
        return f"{koefficient} {stof}" if koefficient != 1 else stof

    reaktanter = [led(forbindelse, formel)]
    produkter = [led(kuldioxid, "CO2"), led(vand, "H2O")]

    if oxygenkoefficient > 0:
        reaktanter.append(led(ilt, "O2"))
    elif oxygenkoefficient < 0:
        produkter.append(led(ilt, "O2"))

    return " + ".join(reaktanter) + " -> " + " + ".join(produkter)


# --- STREAMLIT BRUGERFLADE ---
def main() -> None:
    # Sætter sidens titel og ikon i browser-fanen
    st.set_page_config(page_title="Afstem forbrænding", page_icon="🧪")

    # Overskrift og introduktion (svarer til Titel.TLabel og Tekst.TLabel)
    st.title("Afstem forbrændingsreaktion")
    st.write("Indtast en formel med carbon, hydrogen og oxygen.")

    # Inputfelt (svarer til ttk.Entry) - default værdi er sat til C6H12O6
    formel_felt = st.text_input(
        "Kemisk formel:", value="C6H12O6", placeholder="f.eks. C6H12O6"
    )

    # Knap til at beregne (svarer til ttk.Button)
    if st.button("Beregn reaktion", type="primary"):
        if formel_felt:
            try:
                # Beregner resultatet
                resultat = afstem_forbraending(formel_felt)
                # Viser resultatet i en flot blå boks (svarer til Reaktion.TLabel)
                st.info(f"**Afstemt reaktionsligning:**\n\n`{resultat}`")
            except ValueError as fejl:
                # Viser fejlmeddelelsen i en rød boks (svarer til fejltekst)
                st.error(f"Ugyldig formel: {fejl}")
        else:
            st.warning("Indtast venligst en formel først.")


if __name__ == "__main__":
    main()
