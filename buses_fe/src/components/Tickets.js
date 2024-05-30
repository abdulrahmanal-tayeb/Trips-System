import { useEffect, useState } from "react";
import { baseUrl } from "../helpers/helpers";
import Table from "../helpers/Table";
import MidScreen from "../helpers/MidScreen";

export default function Tickets() {
    const [mode, setMode] = useState("fetching");
 
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