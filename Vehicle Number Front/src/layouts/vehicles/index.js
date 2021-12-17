/**
 * @author Sahan Dinuka
 * @CreatedBy IntelliJ IDEA
 * @created 13/12/2021 - 1:01 PM
 */
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import DataTable from "examples/Tables/DataTable";
import {vehicleTable} from '../../const/tables'
import {strings} from "../../const/strings";
import AddNew from './addNew'
import React, {Component} from "react";
import {getAllVehicles} from "../../services/vehicle";

const data = vehicleTable

class Vehicles extends Component {

    componentDidMount() {
        getAllVehicles().then(res => {
            console.log(res)
        })
    }

    render() {
        return (
            <DashboardLayout>
                <DashboardNavbar/>
                <div align={'right'}>
                    <AddNew/>
                </div>
                <MDBox pt={6} pb={3}>
                    <Grid container spacing={6}>
                        <Grid item xs={12}>
                            <Card>
                                <MDBox
                                    mx={2}
                                    mt={-3}
                                    py={3}
                                    px={2}
                                    variant="gradient"
                                    bgColor="info"
                                    borderRadius="lg"
                                    coloredShadow="info"
                                >
                                    <MDTypography variant="h6" color="white">
                                        All Vehicles Data
                                    </MDTypography>
                                </MDBox>
                                <MDBox pt={3}>
                                    <DataTable
                                        table={data}
                                        isSorted={false}
                                        entriesPerPage={false}
                                        showTotalEntries={false}
                                        noEndBorder
                                    />
                                </MDBox>
                            </Card>
                        </Grid>
                    </Grid>
                </MDBox>
                <Footer/>
            </DashboardLayout>
        );
    }
}

export default Vehicles;
