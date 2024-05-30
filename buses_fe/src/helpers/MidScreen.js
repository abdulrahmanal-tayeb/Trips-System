export default function MidScreen({ children }) {
    return (
        <div style={{ display: "flex", justifyContent: "center", alignContent: "center", position: "fixed", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }}>
            {children}
        </div>
    )
}