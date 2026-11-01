import cv2
from pathlib import Path


class ProcesareImagine:
    def __init__(self, cale):
        self.imagine = cv2.imread(str(cale))
        self.folder = Path(__file__).parent

    def inspectare_imagine(self):
        if self.imagine is None:
            print("Imaginea nu a putut fi incarcata.")
            return False

        inaltime, latime, canale = self.imagine.shape

        print(f"Dimensiuni: {latime} x {inaltime}")
        print(f"Numar de canale: {canale}")
        print(f"Tip date: {self.imagine.dtype}")
        print(f"Total pixeli: {latime * inaltime}")

        cv2.imshow("Imagine originala", self.imagine)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return True

    def conversie_gri(self):
        imagine_gri = cv2.cvtColor(self.imagine, cv2.COLOR_BGR2GRAY)

        print(f"Imagine originala: {self.imagine.shape}")
        print(f"Imagine grayscale: {imagine_gri.shape}")

        # dispare o dimensiune deoarece imaginea gri are un singur canal de culoare
        cv2.imwrite(str(self.folder / "imagine_gri.jpg"), imagine_gri)

        print("Imagine salvata: imagine_gri.jpg")

        return imagine_gri

    def redimensionare(self, procent=0.5):
        print(f"Dimensiune inainte de resize: {self.imagine.shape}")

        imagine_redim = cv2.resize(self.imagine, None, fx=procent, fy=procent)

        print(f"Dimensiune dupa resize: {imagine_redim.shape}")

        cv2.imwrite(str(self.folder / "imagine_redimensionata.jpg"), imagine_redim)

        return imagine_redim

    def decupare(self, x1, x2, y1, y2, procent=0.5):
        imagine_redim = self.redimensionare(procent)

        imagine_decupata = imagine_redim[y1:y2, x1:x2]

        print(f"Dimensiune dupa decupare: {imagine_decupata.shape}")

        cv2.imwrite(str(self.folder / "imagine_decupata.jpg"), imagine_decupata)

        return imagine_decupata

    def desenare_forme(self):
        imagine_desen = self.imagine.copy()

        inaltime, latime, canale = imagine_desen.shape

        # desenez un dreptunghi albastru
        cv2.rectangle(
            imagine_desen,
            (latime // 10, inaltime // 10),
            (latime // 3, inaltime // 3),
            (255, 0, 0),
            3
        )

        # desenez un cerc rosu umplut
        cv2.circle(
            imagine_desen,
            (latime // 2, inaltime // 2),
            min(latime, inaltime) // 10,
            (0, 0, 255),
            -1
        )

        # desenez o linie verde
        cv2.line(
            imagine_desen,
            (0, 0),
            (latime - 1, inaltime - 1),
            (0, 255, 0),
            3
        )

        # scriu textul step it
        cv2.putText(
            imagine_desen,
            "Step IT",
            (latime // 10, inaltime // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            3
        )

        cv2.imwrite(str(self.folder / "imagine_forme.jpg"), imagine_desen)

        print("Imagine salvata: imagine_forme.jpg")

        return imagine_desen

    def rotire_oglindire(self):
        print(f"Imagine originala: {self.imagine.shape}")

        imagine_rotita = cv2.rotate(self.imagine, cv2.ROTATE_90_CLOCKWISE)

        imagine_orizontala = cv2.flip(self.imagine, 1)
        imagine_verticala = cv2.flip(self.imagine, 0)

        print(f"Dupa rotire 90 grade: {imagine_rotita.shape}")
        print(f"Dupa oglindire orizontala: {imagine_orizontala.shape}")
        print(f"Dupa oglindire verticala: {imagine_verticala.shape}")

        cv2.imwrite(str(self.folder / "imagine_rotita.jpg"), imagine_rotita)
        cv2.imwrite(str(self.folder / "imagine_orizontala.jpg"), imagine_orizontala)
        cv2.imwrite(str(self.folder / "imagine_verticala.jpg"), imagine_verticala)

        print("Imaginile au fost salvate.")

        return imagine_rotita, imagine_orizontala, imagine_verticala

    def blur_margini(self, kernel=(5, 5), prag1=100, prag2=200):
        imagine_gri = cv2.cvtColor(self.imagine, cv2.COLOR_BGR2GRAY)

        imagine_blur = cv2.GaussianBlur(imagine_gri, kernel, 0)

        imagine_margini = cv2.Canny(imagine_blur, prag1, prag2)

        # daca maresc kernelul, imaginea devine mai neclara si se pierd detaliile fine

        cv2.imshow("Imagine originala", imagine_gri)
        cv2.imshow("Imagine blur", imagine_blur)
        cv2.imshow("Imagine margini", imagine_margini)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cv2.imwrite(str(self.folder / "imagine_originala_gri.jpg"), imagine_gri)
        cv2.imwrite(str(self.folder / "imagine_blur.jpg"), imagine_blur)
        cv2.imwrite(str(self.folder / "imagine_margini.jpg"), imagine_margini)

        print("Imaginile au fost salvate.")

        return imagine_blur, imagine_margini


if __name__ == "__main__":

    """
    PARTEA a III-a – OPENCV
    Folosiți o imagine la alegere, salvată în același folder cu programul.
    Fiecare rezultat vizual se salvează pe disc cu cv2.imwrite().
    Exercițiul 15 – Citirea și inspectarea unei imagini
    Încarcă o imagine de pe disc și afișează informații despre ea.
    Cerințe:
    1. Citește imaginea cu cv2.imread().
    2. Verifică dacă imaginea a fost încărcată corect; dacă nu,
     afișează un mesaj de eroare și oprește programul.
    3. Afișează lățimea și înălțimea imaginii.
    4. Afișează numărul de canale de culoare și tipul de date.
    5. Afișează imaginea într-o fereastră.
    Output:
    Dimensiuni: 600 x 400
    Numar de canale: 3
    Tip date: uint8
    Total pixeli: 240000
    """

    #task15
    print("---------task15")

    cale = Path(__file__).parent / "Screenshot 2026-10-21 at 12.51.34.png"
    imagine = ProcesareImagine(cale)

    if not imagine.inspectare_imagine():
        exit()

    """
    Exercițiul 16 – Conversia în tonuri de gri
    Transformă o imagine color într-una alb-negru.
    Cerințe:
    1. Încarcă imaginea color.
    2. Convertește imaginea în tonuri de gri cu cv2.cvtColor().
    3. Afișează dimensiunile imaginii înainte și după conversie.
    4. Explică printr-un comentariu în cod de ce dispare o dimensiune.
    5. Salvează rezultatul sub numele imagine
    _gri.jpg.
    Output:
    Imagine originala: (400, 600, 3)
    Imagine grayscale: (400, 600)
    Imagine salvata: imagine
    _gri.jpg
    """

    #task16
    print("---------task16")

    imagine.conversie_gri()

    """
    Exercițiul 17 – Redimensionare și decupare
    Modifică dimensiunile unei imagini și extrage o porțiune din ea.
    Cerințe:
    1. Încarcă o imagine.
    2. Redimensioneaz-o la jumătate din dimensiunea originală, folosind
    cv2.resize().
    3. Decupează un dreptunghi din imagine, folosind indexarea NumPy.
    4. Afișează dimensiunile pentru toate cele trei variante.
    5. Salvează imaginea redimensionată și pe cea decupată.
    Output:
    Dimensiune originala: 600 x 400
    Dimensiune redimensionata: 300 x 200
    Dimensiune decupata: 200 x 150
    Indiciu: decuparea se face cu imagine[y1:y2, x1:x2] – întâi rândurile
      (axa verticală), apoi coloanele.
    """

    #task17
    print("---------task17")

    inaltime, latime, canale = imagine.imagine.shape

    latime_redim = round(latime * 0.5)
    inaltime_redim = round(inaltime * 0.5)

    imagine.decupare(
        0,
        latime_redim // 2,
        0,
        inaltime_redim // 2
    )

    """
    Exercițiul 18 – Desenarea formelor și a textului
    Desenează elemente grafice peste o imagine.
    Cerințe:
    1. Încarcă o imagine sau creează una neagră de 400×400 cu NumPy.
    2. Desenează un dreptunghi albastru cu cv2.rectangle().
    3. Desenează un cerc roșu umplut cu cv2.circle().
    4. Desenează o linie verde cu cv2.line().
    5. Scrie textul Step IT pe imagine cu cv2.putText() și salvează rezultatul.
    Atenție: OpenCV folosește ordinea BGR, nu RGB. Albastru este (255, 0, 0),
    iar roșu este (0, 0, 255) – exact invers față de ce vă așteptați.
    5 puncte · Ușor
    """

    #task18
    print("---------task18")

    imagine.desenare_forme()

    """
    Exercițiul 19 – Rotire și oglindire
    Schimbă orientarea unei imagini.
    Cerințe:
    1. Încarcă o imagine și afișează dimensiunile ei.
    2. Rotește imaginea cu 90 de grade folosind cv2.rotate().
    3. Oglindește imaginea pe orizontală cu cv2.flip().
    4. Oglindește imaginea pe verticală.
    5. Afișează dimensiunile după rotire și salvează toate variantele.
    Output:
    Imagine originala: (400, 600, 3)
    Dupa rotire 90 grade: (600, 400, 3)
    De observat: la rotirea cu 90 de grade, lățimea și înălțimea își
    schimbă locul între ele. La oglindire, dimensiunile rămân neschimbate.
    5 puncte · Ușor
    """

    #task19
    print("---------task19")

    imagine.rotire_oglindire()

    """
    Exercițiul 20 – Blur și detectarea marginilor
    Aplică două filtre clasice de procesare a imaginilor.
    Cerințe:
    1. Încarcă o imagine și convertește-o în tonuri de gri.
    2. Aplică un efect de blur cu cv2.GaussianBlur().
    3. Detectează marginile cu cv2.Canny().
    4. Afișează cele trei imagini: originală, blur și margini.
    5. Salvează rezultatele și scrie într-un comentariu ce se întâmplă
    dacă mărești dimensiunea kernelului de blur.
    Indiciu: kernelul de blur trebuie să aibă dimensiuni impare,
    de exemplu (5, 5) sau (15, 15).
    Pentru Canny, porniți de la pragurile 100 și 200 și ajustați-le
    până marginile ies clare.
    5 puncte · Ușor spre mediu
    """

    #task20
    print("---------task20")

    imagine.blur_margini()