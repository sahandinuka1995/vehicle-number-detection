import team2 from "../assets/images/team-2.jpg";
import MDBox from "../components/MDBox";
import MDBadge from "../components/MDBadge";
import MDTypography from "../components/MDTypography";
import team3 from "../assets/images/team-3.jpg";
import team4 from "../assets/images/team-4.jpg";

/**
 * @author Sahan Dinuka
 * @CreatedBy IntelliJ IDEA
 * @created 13/12/2021 - 1:11 PM
 */
export const vehicleTable = {
    columns: [
        {Header: "author", accessor: "author", width: "45%", align: "left"},
        {Header: "function", accessor: "function", align: "left"},
        {Header: "status", accessor: "status", align: "center"},
        {Header: "employed", accessor: "employed", align: "center"},
        {Header: "action", accessor: "action", align: "center"},
    ],
    rows: [
        {
            author: "asds",
            function: "aasdas",
            status: (
                <MDBox ml={-1}>
                    <MDBadge badgeContent="online" color="success" variant="gradient" size="sm"/>
                </MDBox>
            ),
            employed: (
                <MDTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
                    23/04/18
                </MDTypography>
            ),
            action: (
                <MDTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
                    Edit
                </MDTypography>
            ),
        }
    ],
}
