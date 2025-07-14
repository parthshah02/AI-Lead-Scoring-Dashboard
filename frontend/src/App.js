import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Paper,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  CircularProgress,
} from '@mui/material';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    phone_number: '',
    email: '',
    credit_score: '',
    age_group: '18-25',
    family_background: 'Single',
    income: '',
    comments: '',
    consent: false,
  });

  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const ageGroups = ['18-25', '26-35', '36-50', '51+'];
  const familyBackgrounds = ['Single', 'Married', 'Married with Kids'];

  useEffect(() => {
    fetchLeads();
  }, []);

  const fetchLeads = async () => {
    try {
      const response = await axios.get('http://localhost:8000/leads');
      setLeads(response.data);
    } catch (err) {
      console.error('Error fetching leads:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.consent) {
      setError('Please provide consent to process your data');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/score', formData);
      setLeads([...leads, response.data]);
      setFormData({
        phone_number: '',
        email: '',
        credit_score: '',
        age_group: '18-25',
        family_background: 'Single',
        income: '',
        comments: '',
        consent: false,
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Lead Scoring Dashboard
      </Typography>

      <Box sx={{ display: 'flex', gap: 4, mb: 4 }}>
        <Paper sx={{ p: 4, flex: 1 }}>
          <Typography variant="h6" gutterBottom>
            Add New Lead
          </Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Phone Number"
              type="tel"
              value={formData.phone_number}
              onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
              sx={{ mb: 2 }}
              required
            />
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              sx={{ mb: 2 }}
              required
            />
            <TextField
              fullWidth
              label="Credit Score"
              type="number"
              value={formData.credit_score}
              onChange={(e) => setFormData({ ...formData, credit_score: e.target.value })}
              sx={{ mb: 2 }}
              required
            />
            <TextField
              select
              fullWidth
              label="Age Group"
              value={formData.age_group}
              onChange={(e) => setFormData({ ...formData, age_group: e.target.value })}
              sx={{ mb: 2 }}
              required
            >
              {ageGroups.map((group) => (
                <option key={group} value={group}>
                  {group}
                </option>
              ))}
            </TextField>
            <TextField
              select
              fullWidth
              label="Family Background"
              value={formData.family_background}
              onChange={(e) => setFormData({ ...formData, family_background: e.target.value })}
              sx={{ mb: 2 }}
              required
            >
              {familyBackgrounds.map((bg) => (
                <option key={bg} value={bg}>
                  {bg}
                </option>
              ))}
            </TextField>
            <TextField
              fullWidth
              label="Income"
              type="number"
              value={formData.income}
              onChange={(e) => setFormData({ ...formData, income: e.target.value })}
              sx={{ mb: 2 }}
              required
            />
            <TextField
              fullWidth
              label="Comments"
              multiline
              rows={4}
              value={formData.comments}
              onChange={(e) => setFormData({ ...formData, comments: e.target.value })}
              sx={{ mb: 2 }}
            />
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <TextField
                type="checkbox"
                checked={formData.consent}
                onChange={(e) => setFormData({ ...formData, consent: e.target.checked })}
              />
              <Typography sx={{ ml: 1 }}>
                I consent to data processing
              </Typography>
            </Box>
            {error && (
              <Typography color="error" sx={{ mb: 2 }}>
                {error}
              </Typography>
            )}
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={loading}
              sx={{ mt: 2 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Submit Lead'}
            </Button>
          </form>
        </Paper>

        <Paper sx={{ p: 4, flex: 1 }}>
          <Typography variant="h6" gutterBottom>
            Scored Leads
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Email</TableCell>
                  <TableCell>Initial Score</TableCell>
                  <TableCell>Reranked Score</TableCell>
                  <TableCell>Comments</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {leads.map((lead, index) => (
                  <TableRow key={index}>
                    <TableCell>{lead.email}</TableCell>
                    <TableCell>{lead.initial_score.toFixed(2)}</TableCell>
                    <TableCell>{lead.reranked_score.toFixed(2)}</TableCell>
                    <TableCell>{lead.comments}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Box>
    </Container>
  );
}

export default App;
