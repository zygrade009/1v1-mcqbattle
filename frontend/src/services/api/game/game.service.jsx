import axiosInstance from "../api-axios-instance";


/**
 * Fetch all games.
 * @returns {Promise} - Axios response promise with the list of all MCQs.
 */
export const GetGames = async () => {
  
  return await axiosInstance.get(`/games`);
};
/**
 * Create a new game.
 * @param {Object} data
 * @returns {Promise} - Axios response promise with the created MCQ data.
 */
export const CreateGame = async (data) => {
    return await axiosInstance.post(`/games`,data);
};

/**
 * Fetch all requests.
 * @returns {Promise} - Axios response promise with the list of all requests.
 */
export const GetRequests= async ()=> {
     return await axiosInstance.get('/request')
}
/**
 * Create a new request.
 * @param {Object} data
 * @returns {Promise} - Axios response promise with the created MCQ data.
 */
export const CreateRequest = async (data) => {
  return await axiosInstance.post(`/request`,data);
};
/**
 * Delete a join request by ID.
 * @param {number} id - The ID of the join request to delete.
 * @returns {Promise} - Axios response promise indicating the success of the operation.
 */
export const RejectReq = async (id) => {
  return await axiosInstance.delete(`/request/${id}`);
};
