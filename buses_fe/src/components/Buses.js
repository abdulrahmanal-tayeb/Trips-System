import { useEffect, useState } from "react";
import { baseUrl } from "../helpers/helpers";
import Table from "../helpers/Table";
import MidScreen from "../helpers/MidScreen";

export default function Buses() {
    const [mode, setMode] = useState("fetching");
    const [buses, setBuses] = useState(null);

    const updateBuses = (buses) => setBuses(buses);
    useEffect(() => {
        fetch(baseUrl + "/api/v1/buses/")
            .then(response => response.json())
            .then(buses => {
                if (buses) {
                    setMode(null);
                    updateBuses(buses);
                } else {
                    setMode("empty");
                }
            }).catch(e => console.log(e));
    }, []);

    alert("HELLO");
    switch (mode) {
        case "fetching":
            return <MidScreen>
                <h1>Loading...</h1>
            </MidScreen>
        case "empty": 
            return <MidScreen>
                <h1>No Buses Available Yet!</h1>
                <button className="btn btn-primary">Back</button>
            </MidScreen>
        default:
            return (
                <div>
                    <h1>Available Buses</h1>
                    <Table
                        headers={["Name", "Driver", "Capacity", "Next Destination"]}
                        data={buses}
                        mapperFunction={(bus, index) => (
                            <tr key={index}>
                                {["name", "driver", "seats", "destination"].map(fieldName => (
                                    <td key={index}>{bus[fieldName]}</td>
                                ))}
                            </tr>
                        )}
                    />
                </div>
            )
    }
}