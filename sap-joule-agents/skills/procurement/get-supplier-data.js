/**
 * Skill: Get Supplier Data
 * Description: Retrieves supplier master data and performance metrics from S/4HANA
 */

// Mock data for pilot/testing purposes
const MOCK_DATA = {
    "1000123": {
        supplierId: "1000123",
        name: "Acme Corp",
        status: "Active",
        rating: {
            quality: 95,
            delivery: 88,
            overall: 91
        },
        riskProfile: "Low",
        paymentTerms: "Net 30"
    },
    "1000999": {
        supplierId: "1000999",
        name: "Globex Inc",
        status: "Blocked",
        rating: {
            quality: 70,
            delivery: 65,
            overall: 68
        },
        riskProfile: "High",
        paymentTerms: "Net 60"
    }
};

async function handler(event, context) {
    try {
        const { supplierId } = event.data;
        console.log(`Fetching data for supplier: ${supplierId}`);

        // In a real scenario, this would use the SAP Cloud SDK or axios to call the destination
        // const response = await axios.get(`${process.env.S4HANA_URL}/A_Supplier('${supplierId}')`);

        // For pilot, check mock data
        const supplier = MOCK_DATA[supplierId];

        if (!supplier) {
            return {
                status: 404,
                message: `Supplier ${supplierId} not found.`
            };
        }

        return {
            status: 200,
            data: supplier
        };

    } catch (error) {
        console.error("Error fetching supplier data:", error);
        return {
            status: 500,
            message: "Internal server error"
        };
    }
}

module.exports = { handler };
