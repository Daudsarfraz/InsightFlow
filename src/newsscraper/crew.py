from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool


# Initialize the tool
fwt = FileWriterTool() # file writer tool
sdt = SerperDevTool() # Wweb searcher tool
swt = ScrapeWebsiteTool() # web scraper tool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Newsscraper():
	"""Newsscraper crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	
	
	llm = LLM(
    model = "ollama/llama3.2:3b",
    base_url = "http://localhost:11434"
	)


	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def newsRetriver(self) -> Agent:
		return Agent(
			config=self.agents_config['newsRetriver'],
			verbose=True,
			tools = [sdt],
			llm = self.llm
		)

	@agent
	def newsScraper(self) -> Agent:
		return Agent(
			config=self.agents_config['newsScraper'],
			verbose=True, 
			tools = [swt],
			llm = self.llm
		)

	@agent
	def newsSummerizer(self) -> Agent:
		return Agent(
			config=self.agents_config['newsSummerizer'],
			verbose=True, 
			tools = [],
			llm = self.llm
		)
	
	@agent
	def newsFileWriter(self) -> Agent:
		return Agent(
			config=self.agents_config['newsFileWriter'],
			verbose=True, 
			tools = [fwt],
			llm = self.llm
		)
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task

	@task
	def news_retrieve_task(self) -> Task:
		return Task(
			config=self.tasks_config['news_retrieve_task'],
		)

	@task
	def news_Scraper_task(self) -> Task:
		return Task(
			config=self.tasks_config['news_Scraper_task'],
		)
	
	@task
	def news_Summerizer_task(self) -> Task:
		return Task(
			config=self.tasks_config['news_Summerizer_task'],
		)
	
	@task
	def news_File_Writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['news_File_Writer_task'],
			output_file='final_news.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Newsscraper crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
