import React, { useEffect, useState } from "react";
import { Button, Card, List, Spin, message } from "antd";
import { useNavigate } from "react-router-dom";
import { GetRequests,RejectReq } from "../../services/api/game/game.service";

const Requests = () => {
  const [loading, setLoading] = useState(false);
  const [requests, setRequests] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRequests = async () => {
      setLoading(true);
      try {
        const response = await GetRequests();
        setRequests(response.data);
      } catch (err) {
        console.error(err);
        message.error("Failed to fetch join requests.");
      } finally {
        setLoading(false);
      }
    };
    fetchRequests();
  }, []);

  const handleRequestAction = async (requestId, action) => {
    setLoading(true);
    try {
      // Logic for handling accept/reject action
      console.log("Request action");
      // Example logic:
      // await UpdateJoinRequest(requestId, { status: action });
      // message.success(`Request ${action === "accepted" ? "accepted" : "rejected"} successfully!`);
      // setRequests((prev) => prev.filter((req) => req.id !== requestId));
    } catch (err) {
      console.error(err);
      message.error(`Failed to ${action} the request.`);
    } finally {
      setLoading(false);
    }
  };
  const handleRejectAction = async (requestId) => {
    setLoading(true);
    try {
      // Call the RejectReq function to delete the join request
      const response = await RejectReq(requestId);
      
      if (response.status === 204) { // Check if the request was successful
        message.success("Request rejected successfully!");
        
        // Update the UI by removing the rejected request from the list
        setRequests((prev) => prev.filter((req) => req.id !== requestId));
      } else {
        message.error("Failed to reject the request.");
      }
    } catch (err) {
      console.error(err);
      message.error("An error occurred while rejecting the request.");
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="container flex flex-col flex-grow p-4 mx-auto mb-5 align-items-center">
      <div className="flex items-center justify-between">
        <h1 className="mt-5 mb-4 text-2xl font-bold text-center">Join Requests</h1>
      </div>
      {loading ? (
        <Spin size="large" />
      ) : (
        <List
          grid={{ gutter: 16, column: 1 }}
          dataSource={requests}
          renderItem={(request) => (
            <List.Item>
              
              <Card title={`game title: ${request.game}`} className="shadow-lg d-flex">
                <p className="text-lg">participant: {request.user}</p>
               
                <div className="flex justify-end gap-4">
                  <Button
                    type="primary"
                    onClick={() => handleRequestAction(request.id, "accepted")}
                  >
                    Accept
                  </Button>
          
                  <Button
                    type="danger"
                    onClick={() => handleRejectAction(request.id)}
                  >
                    Reject
                  </Button>
                </div>
              </Card>
            </List.Item>
          )}
        />
      )}
    </div>
  );
};

export default Requests;
