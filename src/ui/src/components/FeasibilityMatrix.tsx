import React, { useState } from 'react';
import { Tab, Accordion, Tooltip, Modal, Typography, IconButton, List, ListItem, ListItemText } from '@mui/material';

const MODEL_CLASSES = [
    {
        name: "Random Forest",
        strengths: ["robustness to noise", "capability to handle diverse data types"],
        bestUsedFor: "datasets with high dimensionality and missing values",
        analogies: {
            Pets: {
                description: "Multiple trainers teaching a pet different tricks.",
                reason: "Each tree (trainer) in the forest focuses on a subset of the data or features (tricks)."
            },
            Cars: {
                description: "A team of mechanics each specializing in a specific car part.",
                reason: "Each tree (mechanic) focuses on understanding and fixing a particular subset of the car's issues."
            },
            Cooking: {
                description: "Cooking with multiple chefs each focused on a particular dish in a multi-course meal.",
                reason: "Each tree (chef) focuses on perfecting a particular dish, leading to a well-rounded meal."
            }
        },
        compatibleWith: {
            "Grid Search": "Given its defined hyperparameters range, Grid Search is suitable for Random Forest."
        }
    },
    // ... Similarly structured data for other models
];

const OPTIMIZERS = [
    {
        name: "Grid Search",
        strengths: ["systematic search", "guaranteed to find the best parameter if it exists in the grid"],
        bestUsedFor: "models with fewer hyperparameters and when computational resources are abundant",
        analogies: {
            Pets: {
                description: "Training a pet by trying every possible command combination to get a trick right.",
                reason: "Grid Search exhaustively tries out predefined hyperparameters to find the best combination."
            },
            Cars: {
                description: "Testing every single part of a car to find out the faulty component.",
                reason: "Grid Search examines all provided parameters systematically."
            },
            Cooking: {
                description: "Testing every spice combination to perfect a dish.",
                reason: "Grid Search explores every ingredient combination to find the best taste."
            }
        }
    },
    // ... Similarly structured data for other optimizers
];

const ENSEMBLE_STRATEGIES = [
    {
        name: "Majority Voting",
        strengths: ["reducing overfitting", "leveraging multiple model outputs"],
        bestUsedFor: "scenarios where individual model variances need to be averaged out",
        analogies: {
            Pets: {
                description: "If multiple trainers agree on the best method to teach a trick, then that method is chosen.",
                reason: "Predictions from multiple models are taken, and the most common prediction is chosen."
            },
            Cars: {
                description: "If multiple mechanics agree on a diagnosis, that is the one adopted.",
                reason: "Ensures reliability in model predictions by aggregating multiple opinions."
            },
            Cooking: {
                description: "If most chefs agree on a specific recipe, it's adopted for the restaurant menu.",
                reason: "By consolidating different chefs' inputs, a well-accepted dish is prepared."
            }
        }
    },
    // ... Similarly structured data for other ensemble strategies
];

// Your UI component
const FeasibilityMatrix: React.FC = () => {
    const [selectedAnalogy, setSelectedAnalogy] = useState<"Pets" | "Cars" | "Cooking">("Pets");
    const [activeItem, setActiveItem] = useState<string | null>(null);
    const [openModal, setOpenModal] = useState<boolean>(false);

    const handleOpen = () => setOpenModal(true);
    const handleClose = () => setOpenModal(false);

    const analogyData = activeItem ? (MODEL_CLASSES.concat(OPTIMIZERS).concat(ENSEMBLE_STRATEGIES).find((item) => item.name === activeItem)?.analogies[selectedAnalogy]) : undefined;

    return (
        <>
            <Tab value={selectedAnalogy} onChange={(event, newValue) => setSelectedAnalogy(newValue)} labels={["Pets", "Cars", "Cooking"]} />
            {MODEL_CLASSES.concat(OPTIMIZERS).concat(ENSEMBLE_STRATEGIES).map((item) => (
                <Accordion expanded={activeItem === item.name} onChange={() => setActiveItem(item.name)}>
                    <Typography variant="h5">{item.name}</Typography>
                    {Object.keys(item.compatibleWith || {}).map((compatibleItem) => (
                        <Tooltip title={item.compatibleWith[compatibleItem] || ""}>
                            <IconButton onClick={handleOpen}>
                                {compatibleItem}  {/* Or use an icon representing the item */}
                            </IconButton>
                        </Tooltip>
                    ))}
                </Accordion>
            ))}

            <Modal open={openModal} onClose={handleClose}>
                <List>
                    <ListItem>
                        <ListItemText primary={analogyData?.description} secondary={analogyData?.reason} />
                    </ListItem>
                </List>
            </Modal>
        </>
    );
};

export default FeasibilityMatrix;
