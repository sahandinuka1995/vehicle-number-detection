/**
 * @author Sahan Dinuka
 * @CreatedBy IntelliJ IDEA
 * @created 15/12/2021 - 9:57 PM
 */
import * as React from 'react';
import {Button, Grid} from '@mui/material';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Icon from "@mui/material/Icon";
import {strings} from "../../const/strings";
import MDButton from "../../components/MDButton";
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function FormDialog() {
    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const [age, setAge] = React.useState('');

    const handleChange = (event) => {
        setAge(event.target.value);
    };

    return (
        <div>
            <MDButton variant="gradient" color="dark" onClick={handleClickOpen}>
                <Icon sx={{fontWeight: "bold"}}>add</Icon>
                &nbsp;{strings.addNewVehicle}
            </MDButton>
            <Dialog open={open} onClose={handleClose} maxWidth={'sm'} fullWidth={true}>
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
                            />
                        </Grid>
                        <Grid item md={6}>
                            <Box sx={{minWidth: 120}} style={{marginTop:15}}>
                                <FormControl fullWidth>
                                    <InputLabel id="demo-simple-select-label">Type</InputLabel>
                                    <Select
                                        labelId="demo-simple-select-label"
                                        id="demo-simple-select"
                                        value={age}
                                        label="Age"
                                        onChange={handleChange}
                                        style={{height:40}}
                                    >
                                        <MenuItem value={10}>Bike</MenuItem>
                                        <MenuItem value={20}>Three Wheel</MenuItem>
                                        <MenuItem value={30}>Car</MenuItem>
                                        <MenuItem value={30}>Van</MenuItem>
                                        <MenuItem value={30}>Bus</MenuItem>
                                        <MenuItem value={30}>Lorry</MenuItem>
                                        <MenuItem value={30}>Tiper</MenuItem>
                                    </Select>
                                </FormControl>
                            </Box>
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Cancel</Button>
                    <Button onClick={handleClose}>Subscribe</Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}
