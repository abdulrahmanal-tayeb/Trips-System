import { useCallback, useEffect, useState } from "react";
import { baseUrl } from "../helpers/helpers";
import Table from "../helpers/Table";
import MidScreen from "../helpers/MidScreen";
import { getRequestHeaders } from "../helpers/helpers";
export default function Trips() {
    const [mode, setMode] = useState("fetching");
    const [trips, setTrips] = useState(null);
    const [choosenTrip, setChoosenTrip] = useState(null);
    const [bookData, setBookData] = useState({});
    const updateTrips = (trips) => setTrips(trips);
    useEffect(() => {
        fetch(baseUrl + "/api/v1/trips/")
            .then(response => response.json())
            .then(trips => {
                if (trips) {
                    setMode(null);
                    updateTrips(trips);
                } else {
                    setMode("empty");
                }
            }).catch(e => console.log(e));
    }, []);

    const handleBook = (trip) => {
        setChoosenTrip(trip);
        setMode("book");
    }

    const submitBook = () => {
        fetch(baseUrl + "/api/v1/tickets/", {
            method: "POST",
            body: JSON.stringify({
                trip: choosenTrip.id,
                buyer: bookData.buyer,
                ...getRequestHeaders()
            })
        })
            .then(response => {
                if (response.status === 201) {
                    setMode("done");
                    setTimeout(() => window.location.href = window.location.href, 1000);
                }
                return response.json();
            }).catch(e => console.log("error: ", e))
    }

    switch (mode) {
        case "fetching":
            return <MidScreen>
                <h1>Loading...</h1>
            </MidScreen>
        case "done":
            return <MidScreen>
                <h1>Ticket has been saved successfully!</h1>
            </MidScreen>
        case "empty":
            return <MidScreen>
                <h1>No Trips Available Yet!</h1>
                <button className="btn btn-primary">Back</button>
            </MidScreen>
        case "book":
            return <MidScreen>
                <h1>Book a Seat</h1>
                <input className="form-control" onChange={({ target }) => setBookData(prev => ({ ...prev, buyer: target.value }))} />
                <button className="btn btn-primary" onClick={submitBook}>Book a Ticket</button>
            </MidScreen>
        default:
            return (
                <div>
                    <h1>Available Buses</h1>
                    <Table
                        headers={["Destination", "Date", "Duration", "Current Passengers", "Book"]}
                        data={trips}
                        mapperFunction={(trip, index) => (
                            <tr key={index}>
                                <td key={index}>{trip.bus.destination}</td>
                                {["date", "estimated_trip_time", "passengers"].map(fieldName => (
                                    <td key={index}>{trip[fieldName]}</td>
                                ))}
                                {!trip.is_full && <td key={"can_book"} onClick={handleBook}>Get a Seat</td>}
                            </tr>
                        )}
                    />
                </div>
            )
    }
}