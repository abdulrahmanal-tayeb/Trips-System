export default function Table({headers, data, mapperFunction}) {
    return (
        <table className="table table-striped table-hover">
            <thead>
                <tr>
                    {headers.map((column, index) => (
                        <th key={index}>{column}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {data.map(mapperFunction)}
            </tbody>
        </table>
    )
}

/*
(row, index) => (
                    <tr key={index}>
                        {columns.map((column, columnIndex) => (
                            <td key={columnIndex}>{row[column.key]}</td>
                        ))}
                    </tr>
                )*/