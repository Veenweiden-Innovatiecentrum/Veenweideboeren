/* v4 programmavoorstel — echte inhoud, met verwijzing naar de toolbox */

const PROGRAMMA = window.PROGRAMMA_CONTENT;

function ProgrammaPagina({ openToolbox, openVisie }) {
  React.useEffect(() => { window.scrollTo(0, 0); }, []);
  return (
    <div data-screen-label="Programmavoorstel">
      <article className="v4-doc">
        {PROGRAMMA.map((s) => <Html key={s.id} html={s.html}></Html>)}
      </article>
      <div style={{ maxWidth: 760, margin: '36px auto 0', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        <DocCard naam="de visie" sub="het verhaal achter dit programma — waarom de veenweideboer de motor is voor de maatschappelijke opgaves" onClick={openVisie}></DocCard>
        <DocCard naam="de toolbox" sub="alle maatregelen als fiches — de instrumenten waarmee de doelen gehaald worden" onClick={openToolbox}></DocCard>
      </div>
    </div>
  );
}

Object.assign(window, { ProgrammaPagina });
