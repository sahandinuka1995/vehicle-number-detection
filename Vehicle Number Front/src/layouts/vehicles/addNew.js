/**
 * @author Sahan Dinuka
 * @CreatedBy IntelliJ IDEA
 * @created 15/12/2021 - 9:57 PM
 */
import React, {Component} from 'react';
import {Button, Grid} from '@mui/material';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Icon from "@mui/material/Icon";
import {strings} from "../../const/strings";
import MDButton from "../../components/MDButton";
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import {addVehicle} from '../../services/vehicle'

export default class AddVehicle extends Component {

    state = {
        open: false,
        vehicleNo: '',
        model: '',
        colour: '',
        type: ''
    }

    handleClickOpen = (state) => {
        this.setState({
            open: state
        })
    };

    onInputHandler = (e) => {
        let val = e.target.value

        this.setState({
            [e.target.name]: val
        })
    }

    onSubmit = async () => {
        let state = this.state
        let data = {
            name: 'Sahan',
            vehicleNo: state.vehicleNo,
            model: state.model,
            colour: state.colour,
            type: state.type
        }

        await addVehicle(data).then((res) => {
            if (res.data.success) {
                this.props.loadAll()
                this.handleClickOpen(false)
            }
        })
    }


    render() {

        return (
            <div>
                <MDButton variant="gradient" color="dark" onClick={() => this.handleClickOpen(true)}>
                    <Icon sx={{fontWeight: "bold"}}>add</Icon>
                    &nbsp;{strings.addNewVehicle}
                </MDButton>
                <Dialog open={this.state.open} onClose={() => this.handleClickOpen(false)} maxWidth={'sm'}
                        fullWidth={true}>
                    <DialogTitle>{strings.addNewVehicle}</DialogTitle>
                    <DialogContent>
                        <Grid container spacing={2}>
                            <Grid item md={6}>
                                <TextField
                                    autoFocus
                                    margin="dense"
                                    id="name"
                                    label={strings.vehicleNo}
                                    type="text"
                                    fullWidth
                                    variant="standard"
                                    onChange={this.onInputHandler}
                                    name={'vehicleNo'}
                                />
                            </Grid>
                            <Grid item md={6}>
                                <TextField
                                    autoFocus
                                    margin="dense"
                                    id="name"
                                    label={strings.model}
                                    type="text"
                                    fullWidth
                                    variant="standard"
                                    onChange={this.onInputHandler}
                                    name={'model'}
                                />
                            </Grid>
                            <Grid item md={6}>
                                <TextField
                                    autoFocus
                                    margin="dense"
                                    id="name"
                                    label={strings.colour}
                                    type="text"
                                    fullWidth
                                    variant="standard"
                                    onChange={this.onInputHandler}
                                    name={'colour'}
                                />
                            </Grid>
                            <Grid item md={6}>
                                <Box sx={{minWidth: 120}} style={{marginTop: 15}}>
                                    <FormControl fullWidth>
                                        <InputLabel id="demo-simple-select-label">Type</InputLabel>
                                        <Select
                                            labelId="demo-simple-select-label"
                                            id="demo-simple-select"
                                            label="Age"
                                            onChange={this.onInputHandler}
                                            style={{height: 40}}
                                            name={'type'}
                                        >
                                            <MenuItem value={'BIKE'}>Bike</MenuItem>
                                            <MenuItem value={'THREE_WHEEL'}>Three Wheel</MenuItem>
                                            <MenuItem value={'CAR'}>Car</MenuItem>
                                            <MenuItem value={'VAN'}>Van</MenuItem>
                                            <MenuItem value={'BUS'}>Bus</MenuItem>
                                            <MenuItem value={'LORRY'}>Lorry</MenuItem>
                                            <MenuItem value={'TIPER'}>Tiper</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Box>
                            </Grid>
                        </Grid>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleClickOpen(false)}>Cancel</Button>
                        <Button onClick={this.onSubmit}>Save</Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}
